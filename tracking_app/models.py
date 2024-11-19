from django.db import models
from django.contrib.auth.models import User



class Task(models.Model):
    status_choices = [
        ('not_started', 'Не начато'),
        ('in_progress', 'В процессе'),
        ('completed', 'Сделано')
    ]

    priority_choices = [
        ('low', 'Низкий'),
        ('medium', 'Средний'),
        ('high', 'Высокий')
    ]

    title = models.CharField(max_length=255, name="title")
    description = models.TextField(name="description")
    status = models.CharField(max_length=20, choices=status_choices, default='not_started', name="status")
    priority = models.CharField(max_length=10, choices=priority_choices, default='medium', name="priority")
    deadline = models.DateTimeField(null=True, blank=True, name="deadline")
    user = models.ForeignKey(User, on_delete=models.CASCADE, name="user")


class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveIntegerField(default=0)
    file = models.FileField(upload_to='comments_files/', blank=True, null=True)

    def __str__(self):
        return f'Comment by {self.author} on {self.task}'


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name='comment_likes'
    )

    class Meta:
        unique_together = ('user', 'comment')

