from django.contrib import admin
from django.urls import path, include
from .views import UserRegistration

urlpatterns = [
    path('home/', UserRegistration.as_view({'post':'create_user'})),
    path('get_users/', UserRegistration.as_view({'get':'get_users'})),
    path('update_users/', UserRegistration.as_view({'put':'update_user'})),
    path('delete_user/', UserRegistration.as_view({'delete':"delete_user"}))
    # path('get_users/', UserRegistration.as_view({'get':'get_users'})),
    # path('get_users/', UserRegistration.as_view({'get':'get_users'}))
    # path('get_users/', UserRegistration.as_view({'get':'get_users'}))
    # path('get_users/', UserRegistration.as_view({'get':'get_users'}))
    # path('get_users/', UserRegistration.as_view({'get':'get_users'}))


]
