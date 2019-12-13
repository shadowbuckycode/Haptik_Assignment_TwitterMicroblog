from django.urls import path, include, re_path
from django.views.generic.base import TemplateView
from . import views
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('tweet/new/', views.tweet_new, name='tweet_new'),
    path('tweet/', views.tweet_list, name='tweet_list'),
    path('tweet/user/<int:pk>/follow/<int:pk2>/', views.follow, name='follow'),
    path('tweet/user/<int:pk>/', views.user_profile, name='user_profile'),
]
