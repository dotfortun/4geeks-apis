from django.contrib import admin

from django.apps import apps

from .models import TodoItem, TodoUser, TodoApiSetting


@admin.register(TodoUser)
class TodoUserAdmin(admin.ModelAdmin):
    list_display = ["name", "created", "updated"]


@admin.register(TodoItem)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = [
        "user", "label", "is_done",
        "created", "updated"
    ]


@admin.register(TodoApiSetting)
class TodoItemAdmin(admin.ModelAdmin):
    list_display = [
        "label", "value"
    ]
