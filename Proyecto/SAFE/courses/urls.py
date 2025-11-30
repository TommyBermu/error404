from django.urls import path
from . import views

urlpatterns = [
    path("catalog/", views.catalog, name="catalog"),
    path("courses/<int:pk>/", views.course_detail_accessible, name="course_detail_accessible"),
    path("create-exam/", views.create_exam_view, name="create_exam"),
]
