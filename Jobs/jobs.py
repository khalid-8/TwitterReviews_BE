from django.utils import timezone
from TwitterNLP.models import userIpAddress, tweets_sentiment

def update_IPs():
    # Query all the IP addresses in our database
    ips = userIpAddress.objects.all()
    # Iterate through them
    for address in ips:
        # If the expiration date is larger than now delete it
        if timezone.now() > address.expiration_date :
            address.delete()
            # log deletion
    print("completed deleting Ips at {}".format(timezone.now()))


def update_cached_Searchs():
    # Query all Tweets in our database
    tweets = tweets_sentiment.objects.all()
    for tweet in tweets:
        # If the expiration date is larger than now delete it
        if timezone.now() > tweet.expiration_date :
            tweet.delete()
    # log deletion
    print("completed deleting Cached tweets at {}".format(timezone.now()))