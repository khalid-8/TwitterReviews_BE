from django.urls import path
from . import views

urlpatterns = [
    path('first/' , views.Analize.first),
    path('analyze/' , views.Analize.analyze),
    path('twitter/', views.Analize.TwitterSearch)
]