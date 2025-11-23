from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Course, Module, Content
from .forms import QuestionUploadForm
from django.contrib import messages


def catalog(request):
    return render(request, "courses/catalog.html")




def parse_evaluacion(texto: str):
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
                "opciones": []
            }

        elif line.startswith("O:"):
            if pregunta_actual is None:
                raise ValueError("Opción sin pregunta previa")

            _, resto = line.split("O:", 1)
            oid, texto_opt, flag = resto.split("|", 2)

            es_correcta = flag.strip() == "1"

            pregunta_actual["opciones"].append({
                "id": oid.strip(),
                "texto": texto_opt.strip(),
                "es_correcta": es_correcta
            })

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
# Importar la futura función que analizará el archivo

def create_exam_view(request):
    
    if request.method == 'POST':
        form = QuestionUploadForm(request.POST, request.FILES)

        if form.is_valid():
           
            course = form.cleaned_data['course']
            difficulty = form.cleaned_data['difficulty']
            uploaded_file = form.cleaned_data['file']
            
            # --- 4. Lógica de Negocio (Pendiente) ---
            # Aquí llamaremos a 'analyze_questions_file'
            
            messages.success(request, f"¡Formulario válido! Archivo '{uploaded_file.name}' listo para procesar.")

           
            return redirect('create_exam') 
        
        else:
            messages.error(request, "El formulario tiene errores. Por favor, revísalo.")
    
    else:
        
        form = QuestionUploadForm()

   
    return render(request, 'courses/create_exam.html', {
        'form': form
    })
    
    
