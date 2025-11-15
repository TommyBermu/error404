from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import AppUser


def login(request):
    usuarios = AppUser.objects.order_by("id").values("id", "username", "email")
    return render(request, "accounts/login.html", {"usuarios": list(usuarios)})


def profile(request):
    return render(request, "accounts/profile.html")


@require_POST
def user_add(request):
    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    if username and email:
        with transaction.atomic():
            AppUser.objects.create(username=username, email=email)
    return redirect("login")


@require_POST
def user_del(request, pk):
    with transaction.atomic():
        AppUser.objects.filter(pk=pk).delete()
    return redirect("login")
