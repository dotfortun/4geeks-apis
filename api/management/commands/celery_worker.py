import shlex
import subprocess
import sys

from django.core.management.base import BaseCommand
from django.utils import autoreload


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("Starting celery worker with autoreload...")
        autoreload.run_with_reloader(self.restart_celery)

    @staticmethod
    def restart_celery():
        celery_worker_cmd = "celery -A api.celery worker -l INFO"
        cmd = f'pkill -f "{celery_worker_cmd}"'
        if sys.platform == "win32":
            cmd = "taskkill /f /t /im celery.exe"

        subprocess.call(shlex.split(cmd))
        subprocess.call(shlex.split(f"{celery_worker_cmd} --loglevel=info"))
