from datetime import datetime, timedelta

from .models import TodoUser, TodoApiSetting

from django.db.models import Max
from celery import shared_task


@shared_task
def clean_todos():
    del_time, _ = TodoApiSetting.objects.filter(
        label="todo_delete_time"
    ).get_or_create(
        label="todo_delete_time",
        value={"days": 7}
    )

    old_users = TodoUser.objects.annotate(
        last_updated=Max("todos__updated", default=datetime.now())
    ).filter(
        last_updated__lte=datetime.now() - timedelta(**del_time.value)
    ).all()

    print("Deleted TodoUsers:", old_users)

    TodoUser.objects.annotate(
        last_updated=Max("todos__updated", default=datetime.now())
    ).filter(
        last_updated__lte=datetime.now() - timedelta(**del_time.value)
    ).delete()
