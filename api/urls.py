from django.contrib import admin
from django.urls import path, include
from .views import register, login, profile_view, profile_edit

urlpatterns = [
    path('register/', register),
    path('login/', login),
    path('profile/view/', profile_view),
    path('profile/edit/', profile_edit)
]
