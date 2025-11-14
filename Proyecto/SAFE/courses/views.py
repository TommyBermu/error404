from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Course, Module, Content, Exam, Assignment, Material


@login_required
def catalog(request):
    courses = Course.objects.filter(status=Course.CourseStatus.ACTIVE).order_by(
        "-created_at"
    )

    return render(request, "courses/catalog.html", {"courses": courses})
