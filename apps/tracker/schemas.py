from ninja import Schema
from typing import List

# --- Схемы ответа (Out) ---

class TaskOut(Schema):
    id: int
    title: str
    order: int
    column_id: int

class ColumnOut(Schema):
    id: int
    title: str
    order: int
    # Вложенные задачи для конкретной колонки
    tasks: List[TaskOut]

class BoardOut(Schema):
    id: int
    title: str
    # Вложенные колонки доски
    columns: List[ColumnOut]

# --- Схемы запроса (In) ---

class TaskMoveIn(Schema):
    task_id: int
    new_column_id: int
    new_order: int
