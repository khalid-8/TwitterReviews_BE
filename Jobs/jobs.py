from django.utils import timezone
from TwitterNLP.models import userIpAddress

def update_IPs():
    # Query all the IP addresses in our database
    ips = userIpAddress.objects.all()
    count = 0
    # Iterate through them
    for address in ips:
        # If the expiration date is larger than now delete it
        if timezone.now() > address.expiration_date :
            address.delete()
            # log deletion
    print("completed deleting Ips at {}".format(timezone.now()))