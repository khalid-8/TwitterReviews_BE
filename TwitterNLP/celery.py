# from flask import Flask
# from celery.schedules import crontab

# app = Flask(__name__)

# app.conf.beat_schedule = {
#     # Executes every day at  12:30 pm.
#     'run-every-hour': {
#         'task': 'tasks.elast',
#         'schedule': crontab(minute='*/1'),
#         'args': (),
#     },
# }
from celery import Celery
from celery.schedules import crontab
from django.utils import timezone
from .models import userIpAddress


app = Celery('updateIPsModel', broker="pyamqp://guest@localhost//")
# disable UTC so that Celery can use local time
app.conf.enable_utc = False


@app.task
def update_IPs():
    # Query all the IP addresses in our database
    ips = userIpAddress.objects.all()

    # Iterate through them
    for address in ips:
        # If the expiration date is larger than now delete it
        if address.expiration_date < timezone.now():
            address.delete()
            # log deletion
    print("completed deleting Ips at {}".format(timezone.now()))


app.conf.beat_schedule = {
    # Executes every...
    'run-every-hour': {
        'task': 'celery.update_IPs',
        'schedule': crontab(minute='*/1'),
    },
}