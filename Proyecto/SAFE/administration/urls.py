from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_panel, name="admin_panel"),
    path("create/", views.course_create, name="course_create"),
    path("course/<int:pk>/", views.course_detail, name="course_detail"),
    path("course/<int:pk>/edit/", views.course_update, name="course_update"),
    path(
        "course/<int:course_pk>/modules/create/",
        views.module_create,
        name="module_create",
    ),
    path(
        "modules/<int:module_pk>/content/create/",
        views.content_create,
        name="content_create",
    ),
]
