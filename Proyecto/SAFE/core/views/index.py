from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from ..singletondb import ConexionBD

def index(request):
    cursor = ConexionBD().obtener_cursor()
    cursor.execute("SELECT id, name, email FROM app_user ORDER BY id;")
    usuarios = [{"id": r[0], "name": r[1], "email": r[2]} for r in cursor.fetchall()]
    return render(request, "index.html", {"usuarios": usuarios})

@require_POST
def user_add(request):
    name = request.POST.get("name", "").strip()
    email = request.POST.get("email", "").strip()
    if name:
        cursor = ConexionBD().obtener_cursor()
        cursor.execute("INSERT INTO app_user (name, email) VALUES (%s, %s);", [name, email or None])
    return redirect("index")

def user_del(request, pk):
    cursor = ConexionBD().obtener_cursor()
    cursor.execute("DELETE FROM app_user WHERE id = %s;", [pk])
    return redirect("index")
