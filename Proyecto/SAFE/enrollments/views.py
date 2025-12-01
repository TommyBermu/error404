from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from enrollments.services import get_courses_for_user, get_paths_for_user


@login_required
def home(request):
    """Dashboard básico de aprendizaje usando visibilidad RF5."""
    courses = get_courses_for_user(request.user)
    paths = get_paths_for_user(request.user)
    return render(
        request,
        "enrollments/home.html",
        {"courses": courses, "paths": paths},
    )
