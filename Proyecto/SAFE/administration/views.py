from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import HttpResponse
from django.urls import reverse
from django.db import transaction
from courses.models import Course, Module, Content, Exam
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

    usuarios = AppUser.objects.all().order_by("id")

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
    modules = course.modules.all().order_by("id")  # pyright: ignore[reportAttributeAccessIssue]

    selected_module = None
    module_contents = None
    selected_content = None
    content_edit_form = None
    material_edit_form = None
    module_id = request.GET.get("module")
    if module_id:
        try:
            selected_module = modules.get(pk=module_id)
        except Module.DoesNotExist:
            selected_module = None
        else:
            module_contents = selected_module.contents.select_related(
                "material", "exam"
            ).order_by("order", "created_at")
            content_id = request.GET.get("content")
            if module_contents.exists() and content_id:
                selected_content = module_contents.filter(pk=content_id).first()

            if selected_content:
                content_edit_form = ContentForm(instance=selected_content)
                if selected_content.material:
                    material_edit_form = MaterialForm(
                        instance=selected_content.material
                    )
                else:
                    material_edit_form = MaterialForm()

    # forms for inline use
    module_form = ModuleForm()
    content_form = ContentForm()
    material_form = MaterialForm()

    context = {
        "course": course,
        "modules": modules,
        "selected_module": selected_module,
        "module_contents": module_contents,
        "selected_content": selected_content,
        "module_form": module_form,
        "content_form": content_form,
        "material_form": material_form,
        "content_edit_form": content_edit_form,
        "material_edit_form": material_edit_form,
    }
    return render(request, "administration/course_detail.html", context)


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
        course.delete()
        messages.success(request, f"Curso '{course.name}' eliminado")
        return redirect("admin_panel")

    return render(request, "administration/admin_panel.html")


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
            # redirigir y seleccionar el módulo creado
            return redirect(
                reverse("course_detail", kwargs={"pk": course.pk})
                + f"?module={module.pk}"
            )
    else:
        form = ModuleForm()

    return render(
        request,
        "administration/module_form.html",
        {"form": form, "course": course, "title": "Agregar Módulo"},
    )


@login_required
@require_POST
def module_delete(request, pk):
    module = get_object_or_404(Module, pk=pk)
    course_pk = module.course.pk

    with transaction.atomic():
        module.delete()
    messages.success(request, "Módulo eliminado")
    return redirect("course_detail", pk=course_pk)


# vista de contenido


@login_required
@require_POST
def content_create(request, module_pk):
    module = get_object_or_404(Module, pk=module_pk)
    redirect_url = (
        reverse("course_detail", kwargs={"pk": module.course.pk})
        + f"?module={module.pk}#content-block-new"
    )

    content_form = ContentForm(request.POST)

    # Determinar el tipo esperado según el block_type
    block_type = request.POST.get("block_type")
    expected_type = None
    if block_type == Content.BlockType.IMAGE:
        expected_type = "jpg"
    elif block_type == Content.BlockType.VIDEO:
        expected_type = "mp4"
    elif block_type == Content.BlockType.PDF:
        expected_type = "pdf"

    # Agregar expected_type a los datos del formulario
    material_data = request.POST.copy()
    if expected_type:
        material_data["expected_type"] = expected_type

    material_form = MaterialForm(material_data, request.FILES)

    if content_form.is_valid():
        content = content_form.save(commit=False)
        content.module = module

        block_type = content.block_type
        content.content_type = Content.ContentType.MATERIAL

        if block_type == Content.BlockType.QUIZ:
            # Obtener las preguntas del formulario
            import json

            quiz_questions = request.POST.get("quiz_questions", "[]")
            try:
                questions = json.loads(quiz_questions)
                exam = Exam.objects.create(
                    questions=questions, total_questions=len(questions)
                )
                content.exam = exam
                content.content_type = Content.ContentType.EXAM
            except json.JSONDecodeError:
                messages.error(
                    request, "Error al procesar las preguntas del cuestionario."
                )
                return redirect(redirect_url)
        elif block_type in (
            Content.BlockType.IMAGE,
            Content.BlockType.VIDEO,
            Content.BlockType.PDF,
        ):
            if material_form.is_valid() and material_form.cleaned_data.get("file"):
                material = material_form.save(commit=False)
                # Asignar tipo automáticamente según block_type
                if block_type == Content.BlockType.IMAGE:
                    material.type = "jpg"
                elif block_type == Content.BlockType.VIDEO:
                    material.type = "mp4"
                elif block_type == Content.BlockType.PDF:
                    material.type = "pdf"
                material.save()
                content.material = material
            else:
                # Mostrar errores específicos del formulario de material
                if material_form.errors:
                    for field, field_errors in material_form.errors.items():
                        for error in field_errors:
                            messages.error(request, f"Archivo: {error}")
                else:
                    messages.error(
                        request,
                        "Adjunta un archivo para imágenes, videos o PDFs.",
                    )
                return redirect(redirect_url)

        content.save()
        messages.success(request, "Contenido agregado al módulo.")
        return redirect(redirect_url)

    for field, field_errors in content_form.errors.items():
        for error in field_errors:
            messages.error(request, f"{field}: {error}")

    return redirect(redirect_url)


@login_required
def content_update(request, content_pk):
    content = get_object_or_404(Content, pk=content_pk)
    module = content.module

    if request.method != "POST":
        return redirect(
            reverse("course_detail", kwargs={"pk": module.course.pk})
            + f"?module={module.pk}&content={content.pk}#content-inspector"
        )

    content_form = ContentForm(request.POST, instance=content)
    material_instance = content.material if content.material else None

    # Determinar el tipo esperado según el block_type
    block_type = request.POST.get("block_type")
    expected_type = None
    if block_type == Content.BlockType.IMAGE:
        expected_type = "jpg"
    elif block_type == Content.BlockType.VIDEO:
        expected_type = "mp4"
    elif block_type == Content.BlockType.PDF:
        expected_type = "pdf"

    # Agregar expected_type a los datos del formulario
    material_data = request.POST.copy()
    if expected_type:
        material_data["expected_type"] = expected_type

    material_form = MaterialForm(
        material_data, request.FILES, instance=material_instance
    )

    material_checked = False

    if content_form.is_valid():
        updated_content = content_form.save(commit=False)
        block_type = updated_content.block_type
        updated_content.content_type = Content.ContentType.MATERIAL

        if block_type == Content.BlockType.QUIZ:
            import json

            quiz_questions = request.POST.get("quiz_questions", "[]")

            if not content.exam:
                content.exam = Exam.objects.create(questions=[], total_questions=0)

            try:
                questions = json.loads(quiz_questions)
                # solo actualizar si recibimos preguntas (para evitar borrar si el campo viene vacío por error)
                # a si es una lista vacía intencional
                # asumimos que el frontend siempre envía el estado actual xd
                content.exam.questions = questions
                content.exam.total_questions = len(questions)
                content.exam.save()
            except json.JSONDecodeError:
                messages.error(
                    request, "Error al procesar las preguntas del cuestionario."
                )

            updated_content.exam = content.exam
            updated_content.material = None
            updated_content.content_type = Content.ContentType.EXAM
        elif block_type in (
            Content.BlockType.IMAGE,
            Content.BlockType.VIDEO,
            Content.BlockType.PDF,
        ):
            material_checked = True
            if material_form.is_valid():
                existing_file = material_form.cleaned_data.get("file") or (
                    material_form.instance and material_form.instance.file
                )
                if not existing_file:
                    material_form.add_error(
                        "file",
                        "Adjunta un archivo para imágenes, videos o PDFs.",
                    )
                else:
                    material = material_form.save(commit=False)
                    # Asignar tipo automáticamente según block_type
                    if block_type == Content.BlockType.IMAGE:
                        material.type = "jpg"
                    elif block_type == Content.BlockType.VIDEO:
                        material.type = "mp4"
                    elif block_type == Content.BlockType.PDF:
                        material.type = "pdf"
                    material.save()
                    updated_content.material = material
                    updated_content.exam = None
            # Si el formulario no es válido, no continuar
        else:
            updated_content.material = None
            updated_content.exam = None

        # Solo guardar si no hay errores en el material form cuando se verificó
        if not material_checked or not material_form.errors:
            updated_content.save()
            messages.success(request, "Contenido actualizado.")
    else:
        for field, field_errors in content_form.errors.items():
            for error in field_errors:
                messages.error(request, f"{field}: {error}")

    if material_checked and material_form.errors:
        for field, field_errors in material_form.errors.items():
            for error in field_errors:
                messages.error(request, f"Archivo: {error}")

    next_url = request.POST.get("next")
    if next_url:
        return redirect(next_url)

    return redirect(
        reverse("course_detail", kwargs={"pk": module.course.pk})
        + f"?module={module.pk}&content={content.pk}#content-inspector"
    )


@login_required
@require_POST
def content_delete(request, content_pk):
    content = get_object_or_404(Content, pk=content_pk)
    module = content.module
    course_pk = module.course.pk

    with transaction.atomic():
        content.delete()

    messages.success(request, "Contenido eliminado.")
    return redirect(
        reverse("course_detail", kwargs={"pk": course_pk}) + f"?module={module.pk}"
    )

@login_required
def user_delete(request, pk):
    """
    Elimina un usuario basado en su ID (pk).
    Solo permite acceso a usuarios logueados (idealmente validar rol también).
    """
    # Buscamos el usuario o devolvemos error 404 si no existe
    user_to_delete = get_object_or_404(AppUser, pk=pk)

    # Protección: Evitar que el usuario se elimine a sí mismo
    if user_to_delete == request.user:
        messages.error(request, "No puedes eliminar tu propio usuario.")
        return redirect("admin_panel") # Redirige de vuelta al panel

    if request.method == "POST":
        username = user_to_delete.username
        user_to_delete.delete()
        messages.success(request, f"Usuario '{username}' eliminado correctamente.")
    
    # Redirigimos al panel de administración (asegúrate que 'admin_panel' sea el name en administration/urls.py)
    return redirect("admin_panel")