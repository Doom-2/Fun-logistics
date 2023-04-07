import os
from celery import Celery
from celery.schedules import crontab

# show each Celery app where settings are located
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'google_sheets_to_db.settings')

# create Celery object and name it as 'send_email'
app = Celery('google_sheets_to_db')

# apply all settings that start with the CELERY_ prefix to the 'app' object
app.config_from_object('django.conf:settings', namespace='CELERY')

# Instruction for Celery to search a list of packages for a 'tasks.py' module
app.autodiscover_tasks()

# celery periodic tasks
app.conf.beat_schedule = {
    'update_price_rub_daily_9_am':
        {
            'task': 'orders.tasks.update_price_rub',
            'schedule': crontab(minute=0, hour=9),  # run task every day at 9 am
        },
}
