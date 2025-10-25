from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from . import models

from shared.db import Database

db = Database()

def index(request):
    usuarios = (
        db.manager(models.AppUser)
        .order_by("id")
        .values("id", "username", "email")
    )
    return render(request, "accounts/index.html", {"usuarios": list(usuarios)})

@require_POST
def user_add(request):
    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    if username and email:
        with db.atomic():
            db.manager(models.AppUser).create(username=username, email=email)
    return redirect("index")

def user_del(request, pk):
    with db.atomic():
        db.manager(models.AppUser).filter(pk=pk).delete()
    return redirect("index")
