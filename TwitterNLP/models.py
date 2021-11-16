from django.db import models
from jsonfield import JSONField

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


class peaccmiddle(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

class tweets_sentiments(models.Model):
    total_count: models.IntegerField()
    postive_count: models.IntegerField()
    negative_count: models.IntegerField()
    charts_graph: models.ImageField(blank=True)
    line_graph: models.ImageField(blank=True)
    pie_graph: models.ImageField(blank=True)
