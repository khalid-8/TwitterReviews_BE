from django.urls import path
from . import views

urlpatterns = [
    # path('export/' , views.export),
    path('twitter/', views.Analize.TwitterSearch)
]