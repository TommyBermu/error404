from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import AppUser
from .password_validator import is_valid_password


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
    
    AppUser.objects.create(username="testuser",email="testuser@example.com",password="testpassword",first_name="Test",last_name="User")   

    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()
    if not unique_email(email):
        AppUser.objects.filter(email="testuser@example.com").delete()  # Eliminar usuario de prueba
        messages.error(request, "Email no existente")
        return redirect("login")

    user = AppUser.objects.get(email=email)
    if user.password != password:
        AppUser.objects.filter(email="testuser@example.com").delete()  # Eliminar usuario de prueba
        messages.error(request, "Contraseña incorrecta")
        return redirect("login")
    
    AppUser.objects.filter(email="testuser@example.com").delete()  # Eliminar usuario de prueba
    return redirect("catalog")



def unique_email(email):
    " Verifica si el email existe en la base de datos "
    try:
        AppUser.objects.get(email = email)
        return True
    except AppUser.DoesNotExist:
        return False


def to_signup(request):
    return render(request, "accounts/sign_up.html")

def to_login(request):
    return render(request, "accounts/login.html")
      
      
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
        error_msg = "La contrase�a debe cumplir con todos los requisitos:\n" \
            "- M�nimo 8 caracteres\n" \
            "- M�nimo una may�scula\n" \
            "- M�nimo una min�scula\n" \
            "- M�nimo un n�mero\n" \
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
