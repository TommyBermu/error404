from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Course, Module, Content
from shared.db import Database

db = Database()

def catalog(request):
    usuarios = (
        db.manager(Course)
        .order_by("id")
        .values("id", "name", "description")
    )
    return render(request, "courses/catalog.html", {"usuarios": list(usuarios)})