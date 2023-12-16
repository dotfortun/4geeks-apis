from datetime import datetime

from django.db import models

# Create your models here.

class TodoUser(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        null=False,
    )
    created = models.DateTimeField(auto_created=True)


class TodoItem(models.Model):
    user = models.ForeignKey(
        "TodoUser",
        on_delete=models.CASCADE,
        related_name="todos",
    )
    label = models.CharField(max_length=256)
    is_done = models.BooleanField(default=False)
    created = models.DateTimeField(auto_created=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created"]
