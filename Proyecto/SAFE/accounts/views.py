from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import AppUser
from .password_validator import is_valid_password
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout


def login(request):
    " Muestra el formulario de inicio de sesion"
    return render(request, "accounts/login.html")
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
    " Loguea al usuario si el email y contrasena son correctos"
    
    
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()
    if not exisit_email(email):
        messages.error(request, "Email no existente")
        return redirect("login")

    user = AppUser.objects.get(email=email)
    if not user.check_password(password):  
        messages.error(request, "Contraseña incorrecta")
        return redirect("login")
    
    auth_login(request, user)
    return redirect("catalog")



def exisit_email(email):
    " Verifica si el email existe en la base de datos "
    try:
        AppUser.objects.get(email = email)
    except AppUser.DoesNotExist:
        return False
    return True


def unique_email(email):
    """Retorna True si existe un usuario con el email dado."""

    return AppUser.objects.filter(email=email).exists()

def to_signup(request):
    return render(request, "accounts/sign_up.html")

def to_login(request):
    return render(request, "accounts/login.html")
      
      
@require_POST
def user_add(request):
    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()
    first_name = request.POST.get("first_name", "").strip()
    last_name = request.POST.get("last_name" , "").strip()

    if not (username and email and password):
        return redirect("signup")

    if AppUser.objects.filter(username=username).exists():
        error_msg = "Este nombre de usuario ya existe. \n Intenta con un nombre distinto"
        return render(request, "accounts/sign_up.html", {
            "usuarios": list(AppUser.objects.order_by("id").values("id", "username", "email", "password")),
            "error_msg": error_msg,
            "username": username,
            "email": email,
        })
    
    if  exisit_email(email):
        error_msg = "Este email ya está registrado. \n Intenta con un email distinto"
        print(error_msg)
        return render(request, "accounts/sign_up.html", {
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
        return render(request, "accounts/sign_up.html", {
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


def logout(request):
    auth_logout(request)
    return redirect("login")
