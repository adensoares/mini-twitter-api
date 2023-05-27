from django.urls import path

from . import views

app_name = 'tweets'

urlpatterns = [
    path('create/', views.create_tweet, name='create_tweet'),
    path('feed/general/', views.general_feed, name='general_feed'),
    path('feed/personalized/', views.personalized_feed, name='personalized_feed'),
]
