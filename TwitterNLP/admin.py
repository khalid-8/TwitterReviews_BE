from django.contrib import admin

# Register your models here.
from .models import peaccmiddle, tweets_sentiment

admin.site.register(peaccmiddle)
admin.site.register(tweets_sentiment)