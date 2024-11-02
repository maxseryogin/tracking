from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    status_choices = [
        ('not_started', 'Не розпочато'),
        ('in_progress', 'В процесі'),
        ('completed', 'Зроблено')
    ]

    priority_choices = [
        ('low', 'Низький'),
        ('medium', 'Середній'),
        ('high', 'Високий')
    ]

    title = models.CharField(max_length=255, name="title")
    description = models.TextField(name="description")
    status = models.CharField(max_length=20, choices=status_choices, default='not_started', name="status")
    priority = models.CharField(max_length=10, choices=priority_choices, default='medium', name="priority")
    deadline = models.DateTimeField(null=True, blank=True, name="deadline")
    user = models.ForeignKey(User, on_delete=models.CASCADE, name="user")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, name="category")

