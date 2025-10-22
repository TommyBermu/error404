from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from ..models import AppUser

def index(request):
    usuarios = AppUser.objects.order_by("id").values("id", "name", "email")
    return render(request, "index.html", {"usuarios": list(usuarios)})

@require_POST
def user_add(request):
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    if name:
        AppUser.objects.create(name=name, email=email)
    return redirect("index")

def user_del(request, pk):
    AppUser.objects.filter(pk=pk).delete()
    return redirect("index")
