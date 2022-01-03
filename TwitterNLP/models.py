from django.db import models
from jsonfield import JSONField
from django.utils import timezone

# Create your models here.
class tweets_sentiment(models.Model):
    search_term = models.CharField(max_length=120)
    total_count = models.IntegerField()
    postive_count = models.IntegerField()
    negative_count = models.IntegerField()
    postive_tweets = JSONField()
    negative_tweets = JSONField()
    charts_graph = models.ImageField(blank=True)
    line_graph = models.ImageField(blank=True)
    pie_graph = models.ImageField(blank=True)


class userIpAddress(models.Model):
    created_at = models.DateTimeField(default=timezone.now)
    ip_address = models.CharField(max_length=20)
    number_of_requests = models.IntegerField(default=1, blank=True)
    expiration_date = models.DateTimeField()


