from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from . import models

from shared.db import Database

db = Database()

def catalog(request):
    usuarios = (
        db.manager(models.Course)
        .order_by("id")
        .values("id", "name", "description")
    )
    return render(request, "courses/catalog.html", {"usuarios": list(usuarios)})