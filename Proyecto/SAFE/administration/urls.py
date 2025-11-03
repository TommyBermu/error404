from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_panel, name='admin_panel'),
]