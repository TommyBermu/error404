from django.urls import path
from .views import *

urlpatterns = [
    path("", index, name="index"),
    path("users/add/", user_add, name="user_add"),
    path("users/<int:pk>/del/", user_del, name="user_del"),
]