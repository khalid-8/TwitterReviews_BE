from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import update_IPs


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(update_IPs, 'interval', hours=24, id="eligibility_check", name='update_ipAddresses', jobstore='default')
    scheduler.start()