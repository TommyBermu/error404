# SAFE/core/urls.py
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('singleton-example/', views.SingletonExampleView.as_view(), name='singleton_example'),
    path('health/', views.health_check, name='health_check'),
]
