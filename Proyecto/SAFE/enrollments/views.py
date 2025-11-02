from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from . import models

from shared.db import Database

db = Database()

def home(request):
    return render(request, "enrollments/home.html")