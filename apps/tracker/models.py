from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Board(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Column(models.Model):
    board = models.ForeignKey(Board, related_name='columns', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)  # 'To Do', 'In Progress'
    order = models.PositiveIntegerField(default=0)  # Для сортировки колонок

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.board.name} - {self.name}"


class Task(models.Model):
    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    )

    column = models.ForeignKey(Column, related_name='tasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    assignee = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name='tasks')
    order = models.PositiveIntegerField(default=0)  # Для Drag-and-Drop сортировки внутри колонки
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title
