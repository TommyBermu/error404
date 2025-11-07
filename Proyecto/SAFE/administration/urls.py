from django.urls import path
from . import views

urlpatterns = [
    path("", views.admin_panel, name="admin_panel"),
    path("create/", views.course_create, name="course_create"),
    path("<int:pk>/", views.course_detail, name="course_detail"),
    path("<int:pk>/edit/", views.course_update, name="course_update"),
    path("<int:pk>/delete/", views.course_delete, name="course_delete"),
    path("<int:course_pk>/modules/create/", views.module_create, name="module_create"),
    path("modules/<int:pk>/delete/", views.module_delete, name="module_delete"),
    path(
        "modules/<int:module_pk>/content/create/",
        views.content_create,
        name="content_create",
    ),
]
