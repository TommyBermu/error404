
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
   
   #crear usuario de prueba
   
    AppUser.objects.create(username="testuser",email="testuser@example.com",password="testpassword",first_name="Test",last_name="User")   

    email = request.POST.get("email", "").strip()
    password = request.POST.get("password", "").strip()
    if not unique_email(email):
        #messages.error(request, f"Email no encontrado: {email}")
        AppUser.objects.filter(email="testuser@example.com").delete()  # Eliminar usuario de prueba
        return render(request, 'accounts/login.html', {'error_login': 'Email no existente'})

    user = AppUser.objects.get(email=email)
    if user.password != password:
        #messages.error(request, "Contraseña incorrecta")
        AppUser.objects.filter(email="testuser@example.com").delete()  # Eliminar usuario de prueba
        return render(request, 'accounts/login.html', {'error_login': 'Contraseña incorrecta'})
    
    AppUser.objects.filter(email="testuser@example.com").delete()  # Eliminar usuario de prueba
    return redirect("catalog")



def unique_email(email):
    #codigo
    try:
        AppUser.objects.get(email = email)
        return True
    except AppUser.DoesNotExist:
        return False

