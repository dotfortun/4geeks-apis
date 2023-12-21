from datetime import datetime

from django.db import models

# Create your models here.


class TodoUser(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        null=False,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    @property
    def updated(self) -> datetime:
        return max([x.updated for x in self.todos.all()] + [self.created])

    def __str__(self) -> str:
        return self.name


class TodoItem(models.Model):
    user = models.ForeignKey(
        "TodoUser",
        on_delete=models.CASCADE,
        related_name="todos",
    )
    label = models.CharField(max_length=256)
    is_done = models.BooleanField(default=False)
    created = models.DateTimeField(
        auto_now_add=True
    )
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.label

    class Meta:
        ordering = ["created"]


class TodoApiSetting(models.Model):
    label = models.CharField(
        max_length=128,
        unique=True,
        null=False
    )
    value = models.JSONField()

    def __str__(self) -> str:
        return self.label
