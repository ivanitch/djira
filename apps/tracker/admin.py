from django.contrib import admin

from apps.tracker.models import Board, Column, Task

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Board._meta.fields]

@admin.register(Column)
class ColumnAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Column._meta.fields]


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Task._meta.fields]
