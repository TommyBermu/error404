from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from . import models

def index(request):
    usuarios = models.AppUser.objects.order_by("id").values("id", "first_name", "email")
    return render(request, "accounts/index.html", {"usuarios": list(usuarios)})

@require_POST
def user_add(request):
    username = request.POST.get("username", "").strip()
    email = request.POST.get("email", "").strip()
    if username:
        models.AppUser.objects.create(username=username, email=email)
    return redirect("index")

def user_del(request, pk):
    models.AppUser.objects.filter(pk=pk).delete()
    return redirect("index")
