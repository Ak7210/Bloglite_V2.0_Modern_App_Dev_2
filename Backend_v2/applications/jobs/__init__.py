from celery import Celery, Task
from flask import current_app as app
from celery.schedules import crontab

celery = Celery("Jobs", broker='redis://localhost:6379/1', backend='redis://localhost:6379/2', imports=["applications.mail.daily_reminder", "applications.mail.monthly_summary" ])
celery.conf.timezone = 'Asia/Kolkata'


class ContextTask(Task):
    def __call__(self, *args, **kwargs):
        with app.app_context():
            return self.run(*args, **kwargs)
        