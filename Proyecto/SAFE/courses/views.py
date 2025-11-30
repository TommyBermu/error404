from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from enrollments.services import (
    get_contents_for_user_in_course,
    get_courses_for_user,
)
from .forms import QuestionUploadForm
from .models import Content, Course, Exam, Material, Module


def parse_evaluacion(texto: str):
    """Parsea preguntas tipo 'Q:' y opciones 'O:' desde un texto."""
    preguntas = []
    pregunta_actual = None

    for line in texto.splitlines():
        line = line.strip()
        if not line:
            # Línea vacía: separador entre preguntas
            continue

        if line.startswith("Q:"):
            # Guardar pregunta anterior, si había
            if pregunta_actual is not None:
                preguntas.append(pregunta_actual)

            _, resto = line.split("Q:", 1)
            qid, texto_preg = resto.split("|", 1)

            pregunta_actual = {
                "id": qid.strip(),
                "texto": texto_preg.strip(),
                "opciones": [],
            }

        elif line.startswith("O:"):
            if pregunta_actual is None:
                raise ValueError("Opción sin pregunta previa")

            _, resto = line.split("O:", 1)
            oid, texto_opt, flag = resto.split("|", 2)

            es_correcta = flag.strip() == "1"

            pregunta_actual["opciones"].append(
                {"id": oid.strip(), "texto": texto_opt.strip(), "es_correcta": es_correcta}
            )

        else:
            raise ValueError(f"Línea con formato inválido: {line}")

    # Agregar la última pregunta si existe
    if pregunta_actual is not None:
        preguntas.append(pregunta_actual)

    # Validación extra: cada pregunta con al menos una correcta
    for p in preguntas:
        if not any(o["es_correcta"] for o in p["opciones"]):
            raise ValueError(f"La pregunta '{p['id']}' no tiene opción correcta")

    return preguntas


def is_txt_file(uploaded_file) -> bool:
    """
    Verifica si el archivo subido corresponde a un .txt
    usando la extensión del nombre del archivo.
    """
    if not hasattr(uploaded_file, "name"):
        return False
    return uploaded_file.name.lower().endswith(".txt")


def create_exam_view(request):
    if request.method == "POST":
        form = QuestionUploadForm(request.POST, request.FILES)

        if form.is_valid():
            course = form.cleaned_data["course"]
            difficulty = form.cleaned_data["difficulty"]
            uploaded_file = form.cleaned_data["file"]

            # Placeholder: aquí iría la lógica de negocio para analizar el .txt
            messages.success(
                request,
                f"¡Formulario válido! Archivo '{uploaded_file.name}' listo para procesar.",
            )

            return redirect("create_exam")
        else:
            messages.error(request, "El formulario tiene errores. Por favor, revísalo.")

    else:
        form = QuestionUploadForm()

    return render(request, "courses/create_exam.html", {"form": form})


@login_required
def catalog(request):
    """Catálogo visible según el rol del usuario (RF5)."""
    courses = get_courses_for_user(request.user).order_by("-created_at")
    return render(request, "courses/catalog.html", {"courses": courses})


@login_required
def course_detail_accessible(request, pk):
    """Detalle de curso respetando visibilidad de contenidos por rol (RF5)."""
    course = get_object_or_404(Course, pk=pk)

    visible_contents = get_contents_for_user_in_course(request.user, course)
    modules = (
        Module.objects.filter(course=course)
        .prefetch_related("contents", "contents__material", "contents__exam")
        .order_by("id")
    )

    contents_by_module = {module.id: [] for module in modules}
    for content in visible_contents:
        contents_by_module.setdefault(content.module_id, []).append(content)

    modules_with_contents = [
        (module, contents_by_module.get(module.id, [])) for module in modules
    ]

    context = {
        "course": course,
        "modules_with_contents": modules_with_contents,
    }
    return render(request, "courses/course_detail_accessible.html", context)
