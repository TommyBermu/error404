
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import AppUser

def login(request):
    usuarios = (
        AppUser.objects
        .order_by("id")
        .values("id", "username", "email")
    )
    return render(request, "accounts/login.html", {"usuarios": list(usuarios)})
    # try:
    #     AppUser.objects.get(email = request.POST.get("email"))
    # except AppUser.DoesNotExist:
    #     #Mostrar mensaje de advertencia , email no existe
    #     messages.warning(request, "El email no existe")
    #     return False

    # return True

def profile(request):
    return render(request, "accounts/profile.html")

@require_POST
def log(request):
    # username = request.POST.get("username", "").strip()
    # email = request.POST.get("email", "").strip()
    # if username and email:
    #     with transaction.atomic():
    #         AppUser.objects.create(username=username, email=email)
    # return redirect("login")
    email = request.POST.get("email", "").strip()
    if unique_email(email):
        messages.success(request, f"Email encontrado: {email}")
    else:
        messages.error(request, f"Email no encontrado: {email}")
    
    return redirect("login")


def unique_email( email):
    #codigo
    try:
        AppUser.objects.get(email = email)
        return True
    except AppUser.DoesNotExist:
        return False


def user_del(request, pk):
    with transaction.atomic():
        AppUser.objects.filter(pk=pk).delete()
    return redirect("login")
