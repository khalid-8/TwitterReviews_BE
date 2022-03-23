# from django.http import HttpResponse
from django.contrib import admin
# from import_export.admin import ImportExportModelAdmin

# Register your models here.
from .models import userIpAddress, tweets_sentiment

admin.site.register(userIpAddress)
admin.site.register(tweets_sentiment)

# Import and export objects from the tweets_sentiment model in the admin page
# @admin.register(tweets_sentiment)
# class TweetsAdmin(ImportExportModelAdmin):
#     pass