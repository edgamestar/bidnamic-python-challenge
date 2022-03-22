import os

from celery import Celery

# set the default Django settings module for the 'celery' program.

from bidnamic.base_settings import WHOSE

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'bidnamic.settings.{WHOSE}')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')
app = Celery('bidnamic')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
