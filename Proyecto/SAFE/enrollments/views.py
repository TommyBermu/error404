from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from . import models

def home(request):
    return render(request, "enrollments/home.html")