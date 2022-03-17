from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from .jobs import update_IPs, update_cached_Searchs


def start():
    scheduler = BackgroundScheduler()
    #Adding the job: update_ips every hour to delete IP addresses that exceeded the daily limit from the DB
    scheduler.add_job(update_IPs, 'interval', hours=1, id="eligibility_check", name='update_ipAddresses', jobstore='default')
    #Adding the job: update_cached_Searchs every 30 minutes to delete cached tweets from the DB
    scheduler.add_job(update_cached_Searchs, 'interval', minutes=30, id="cached_tweets", name='update_cached_tweets', jobstore='default')
    scheduler.start()