# from celery.schedules import crontab
# from celery.task import periodic_task
# from django.utils import timezone
# from .models import userIpAddress
# import celery

#run crontab task every 3 hours to delete items from the userIpAddress DB
#run_every=crontab(minute=0, hour='*/3')
# @periodic_task(run_every=crontab(minute='*/1'))
# def delete_old_IPs():
#     # Query all the IP addresses in our database
#     ips = userIpAddress.objects.all()

#     # Iterate through them
#     for address in ips:
#         # If the expiration date is larger than now delete it
#         if address.expiration_date < timezone.now():
#             address.delete()
#             # log deletion
#     print("completed deleting Ips at {}".format(timezone.now()))
#     # return 


# from celery import shared_task
# from django.utils import timezone
# from .models import userIpAddress


# @shared_task
# def update_IPs():
#     # Query all the IP addresses in our database
#     ips = userIpAddress.objects.all()

#     # Iterate through them
#     for address in ips:
#         # If the expiration date is larger than now delete it
#         if timezone.now() > address.expiration_date :
#             address.delete()
#             # log deletion
#         print("completed deleting Ips at {}".format(timezone.now()))


# Create your tests here.