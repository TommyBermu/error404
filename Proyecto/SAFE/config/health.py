from django.http import JsonResponse
from shared.db import Database

def db_health(request):
    ok = Database().is_usable()
    return JsonResponse(
        {"DB Status: ": "Healthy" if ok else "Unhealthy"},
        status=200 if ok else 500,
    )