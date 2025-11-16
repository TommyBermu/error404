from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .models import Course, Module, Content
from .forms import QuestionUploadForm
from django.contrib import messages


def catalog(request):
    return render(request, "courses/catalog.html")


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
    
    