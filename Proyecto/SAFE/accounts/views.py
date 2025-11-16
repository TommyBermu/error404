from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import AppUser
from .password_validator import is_valid_password

def login(request):
    usuarios = (
        AppUser.objects
        .order_by("id")
        .values("id", "username", "email", "password")
    )
    return render(request, "accounts/login.html", {"usuarios": list(usuarios)})

def profile(request):
    return render(request, "accounts/profile.html")

@require_POST
def user_add(request):
    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()

    if not (username and email and password):
        return redirect("login")

    if AppUser.objects.filter(username=username).exists():
        error_msg = "Este nombre de usuario ya existe. \n Intenta con un nombre distinto"
        return render(request, "accounts/login.html", {
            "usuarios": list(AppUser.objects.order_by("id").values("id", "username", "email", "password")),
            "error_msg": error_msg,
            "username": username,
            "email": email,
        })

    if not is_valid_password(password):
        error_msg = "La contraseña debe cumplir con todos los requisitos:\n" \
            "- Mínimo 8 caracteres\n" \
            "- Mínimo una mayúscula\n" \
            "- Mínimo una minúscula\n" \
            "- Mínimo un número\n" \
            "- No contener espacios"
        return render(request, "accounts/login.html", {
            "usuarios": list(AppUser.objects.order_by("id").values("id", "username", "email", "password")),
            "error_msg": error_msg,
            "username": username,
            "email": email,
        })

    with transaction.atomic():
        user = AppUser(username=username, email=email)
        user.set_password(password)
        user.save()
    return redirect("login")

def user_del(request, pk):
    with transaction.atomic():
        AppUser.objects.filter(pk=pk).delete()
    return redirect("login")
