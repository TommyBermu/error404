from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from courses.models import Course, Module, Content, Exam, Assignment, Material
from accounts.models import AppUser
from django.contrib import messages
from .forms import CourseForm, ModuleForm, ContentForm, MaterialForm


@login_required
def admin_panel(request):
    if request.user.role != "analistaTH":
        return HttpResponse("No tienes permisos", status=403)

    active_tab = request.GET.get("tab", "cursos")

    courses = Course.objects.all().order_by("-created_at")
    selected_course = None
    selected_module = None

    course_id = request.GET.get("course")
    if course_id:
        selected_course = get_object_or_404(Course, id=course_id)

        module_id = request.GET.get("module")
        if module_id:
            selected_module = get_object_or_404(
                Module, id=module_id, course=selected_course
            )

    learning_paths = []

    usuarios = AppUser.objects.order_by("id").values("id", "username", "email")

    context = {
        "active_tab": active_tab,
        "courses": courses,
        "selected_course": selected_course,
        "selected_module": selected_module,
        "learning_paths": learning_paths,
        "usuarios": usuarios,
    }
    return render(request, "administration/admin_panel.html", context)


@login_required
def course_create(request):
    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.created_by = request.user
            course.save()
            messages.success(request, f"Curso '{course.name}' creado exitosamente")
            return redirect("course_detail", pk=course.pk)
    else:
        form = CourseForm()

    return render(
        request,
        "administration/course_form.html",
        {"form": form, "title": "Crear Curso"},
    )


@login_required
def course_detail(request, pk):
    course = get_object_or_404(Course, pk=pk)
    modules = course.modules.all().order_by("id")

    return render(
        request,
        "administration/course_detail.html",
        {"course": course, "modules": modules},
    )


@login_required
def course_update(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        form = CourseForm(request.POST, request.FILES, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f"Curso '{course.name}' actualizado")
            return redirect("course_detail", pk=course.pk)
    else:
        form = CourseForm(instance=course)

    return render(
        request,
        "administration/course_form.html",
        {"form": form, "title": "Editar Curso", "course": course},
    )


@login_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == "POST":
        course_name = course.name
        course.delete()
        messages.success(request, f"Curso '{course_name}' eliminado")
        return redirect("admin_panel")

    return render(
        request, "administration/course_confirm_delete.html", {"course": course}
    )


# vistas de modulos


@login_required
def module_create(request, course_pk):
    course = get_object_or_404(Course, pk=course_pk)

    if request.method == "POST":
        form = ModuleForm(request.POST)
        if form.is_valid():
            module = form.save(commit=False)
            module.course = course
            module.save()
            messages.success(request, f"Módulo '{module.name}' agregado")
            return redirect("course_detail", pk=course.pk)
    else:
        form = ModuleForm()

    return render(
        request,
        "administration/module_form.html",
        {"form": form, "course": course, "title": "Agregar Módulo"},
    )


@login_required
def module_delete(request, pk):
    module = get_object_or_404(Module, pk=pk)
    course = module.course

    if request.method == "POST":
        module.delete()
        messages.success(request, "Módulo eliminado")
        return redirect("course_detail", pk=course.pk)

    return render(
        request,
        "administration/module_confirm_delete.html",
        {"module": module, "course": course},
    )


# vista de contenido


@login_required
def content_create(request, module_pk):
    module = get_object_or_404(Module, pk=module_pk)

    if request.method == "POST":
        content_form = ContentForm(request.POST)
        content_type = request.POST.get("content_type")

        if content_form.is_valid():
            content = content_form.save(commit=False)
            content.module = module

            # Crear el objeto polimórfico según el tipo
            if content_type == "material":
                material_form = MaterialForm(request.POST, request.FILES)
                if material_form.is_valid():
                    material = material_form.save()
                    content.material = material

            elif content_type == "exam":
                # Aquí puedes agregar lógica para exámenes
                exam = Exam.objects.create()
                content.exam = exam

            elif content_type == "assignment":
                # Lógica para tareas
                assignment = Assignment.objects.create()
                content.assignment = assignment

            content.save()
            messages.success(request, "Contenido agregado al módulo.")
            return redirect("course_detail", pk=module.course.pk)
    else:
        content_form = ContentForm()
        material_form = MaterialForm()

    return render(
        request,
        "administration/content_form.html",
        {
            "content_form": content_form,
            "material_form": material_form,
            "module": module,
            "course": module.course,
        },
    )
