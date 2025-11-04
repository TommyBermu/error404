from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from courses.models import Course, Module, Content
from accounts.models import AppUser

@login_required
def admin_panel(request):
    if request.user.role != 'analistaTH':
        return HttpResponse('No tienes permisos', status=403)
    
    active_tab = request.GET.get('tab', 'cursos')
    
    courses = Course.objects.all().order_by('-created_at')
    selected_course = None
    selected_module = None
    
    course_id = request.GET.get('course')
    if course_id:
        selected_course = get_object_or_404(Course, id=course_id)
        
        module_id = request.GET.get('module')
        if module_id:
            selected_module = get_object_or_404(
                Module, 
                id=module_id, 
                course=selected_course
            )
    
    learning_paths = []
    
    context = {
        'active_tab': active_tab,
        'courses': courses,
        'selected_course': selected_course,
        'selected_module': selected_module,
        'learning_paths': learning_paths,
        'usuarios': AppUser.objects.order_by("id").values("id", "username", "email")
    }
    return render(request, 'administration/admin_panel.html', context)