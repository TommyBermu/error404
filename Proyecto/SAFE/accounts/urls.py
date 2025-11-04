from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("users/add/", views.user_add, name="user_add"),
    path("users/<int:pk>/del/", views.user_del, name="user_del"),
]