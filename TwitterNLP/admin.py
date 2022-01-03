from django.contrib import admin

# Register your models here.
from .models import userIpAddress, tweets_sentiment

admin.site.register(userIpAddress)
admin.site.register(tweets_sentiment)