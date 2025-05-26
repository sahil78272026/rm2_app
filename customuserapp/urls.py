from django.contrib import admin
from django.urls import path, include
from .views import UserRegistration

urlpatterns = [
    path('home/', UserRegistration.as_view({'post':'create_user'}))
]
