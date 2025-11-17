from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login, name="login"),
    path("profile/", views.profile, name="profile"),
    path("users/log", views.log, name="log"),
    path("users/<int:pk>/del/", views.user_del, name="user_del"),
]