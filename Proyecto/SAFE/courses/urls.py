from django.urls import path
from . import views

urlpatterns = [
    path("catalog/", views.catalog, name="catalog"),
    path('create-exam/', views.create_exam_view, name='create_exam'),
]