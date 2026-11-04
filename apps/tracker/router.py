from ninja import Router
from django.shortcuts import get_object_or_404
from django.db.models import Prefetch, F
from django.db import transaction

from .models import Board, Column, Task
from .schemas import BoardOut, TaskMoveIn

router = Router()


@router.get("/boards/{board_id}", response=BoardOut)
def get_board(request, board_id: int):
    # Используем Prefetch для устранения проблемы N+1.
    # За 3 SQL-запроса мы достанем саму доску, все её колонки и все задачи,
    # причем сразу отсортированные по полю order.
    board = get_object_or_404(
        Board.objects.prefetch_related(
            Prefetch(
                'columns',
                queryset=Column.objects.order_by('order')
            ),
            Prefetch(
                'columns__tasks',
                queryset=Task.objects.order_by('order')
            )
        ),
        id=board_id
    )
    return board


@router.post("/tasks/move")
def move_task(request, payload: TaskMoveIn):
    # Оборачиваем в транзакцию, чтобы в случае ошибки база не осталась
    # с дублирующимися значениями order.
    with transaction.atomic():
        task = get_object_or_404(Task, id=payload.task_id)

        old_column_id = task.column_id
        old_order = task.order
        new_column_id = payload.new_column_id
        new_order = payload.new_order

        # Если задачу бросили на то же самое место — ничего не делаем
        if old_column_id == new_column_id and old_order == new_order:
            return {"success": True}

        if old_column_id == new_column_id:
            # Сценарий А: Перемещение внутри одной колонки
            if old_order < new_order:
                # Тащим вниз: сдвигаем промежуточные задачи ВВЕРХ (уменьшаем order)
                Task.objects.filter(
                    column_id=old_column_id,
                    order__gt=old_order,
                    order__lte=new_order
                ).update(order=F('order') - 1)
            else:
                # Тащим вверх: сдвигаем промежуточные задачи ВНИЗ (увеличиваем order)
                Task.objects.filter(
                    column_id=old_column_id,
                    order__gte=new_order,
                    order__lt=old_order
                ).update(order=F('order') + 1)
        else:
            # Сценарий Б: Перемещение в ДРУГУЮ колонку

            # 1. Захлопываем "дыру" в старой колонке (всё, что ниже старого места, едет вверх)
            Task.objects.filter(
                column_id=old_column_id,
                order__gt=old_order
            ).update(order=F('order') - 1)

            # 2. Раздвигаем место в новой колонке (всё, начиная с нового места, едет вниз)
            Task.objects.filter(
                column_id=new_column_id,
                order__gte=new_order
            ).update(order=F('order') + 1)

        # Применяем новые значения к самой перетаскиваемой задаче
        task.column_id = new_column_id
        task.order = new_order
        # update_fields нужен, чтобы не перезаписать другие поля,
        # если их кто-то изменил в этот же момент (защита от race condition)
        task.save(update_fields=['column_id', 'order'])

    return {"success": True}
