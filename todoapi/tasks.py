import logging
from datetime import datetime, timedelta

from .models import TodoUser, TodoApiSetting

from django.db.models import Max, Min
from celery import shared_task


@shared_task
def clean_todos():
    print(__name__)
    del_time, _ = TodoApiSetting.objects.get_or_create(
        label="todo_delete_time",
        defaults={
            "value": {"days": 7}
        }
    )

    old_users = TodoUser.objects.all().annotate(
        last_updated=Min("todos__updated", default=(
            datetime.now() - timedelta(**del_time.value)))
    ).filter(
        last_updated__lte=(datetime.now() - timedelta(**del_time.value))
    )

    print("Deleting old TodoUsers:", [
        (x.name, x.last_updated.isoformat()) for x in old_users])

    TodoUser.objects.all().annotate(
        last_updated=Min("todos__updated", default=(
            datetime.now() - timedelta(**del_time.value)))
    ).filter(
        last_updated__lte=(datetime.now() - timedelta(**del_time.value))
    ).delete()

    print("Old TodoUsers deleted.")
