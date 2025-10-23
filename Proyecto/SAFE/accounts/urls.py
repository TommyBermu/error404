from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/add/", views.user_add, name="user_add"),
    path("users/<int:pk>/del/", views.user_del, name="user_del"),
]