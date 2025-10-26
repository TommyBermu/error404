# SAFE/core/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from config.models import SiteConfiguration
import json

class SingletonExampleView(View):
    """
    Vista de ejemplo que demuestra el uso del patrón Singleton.
    """
    
    def get(self, request):
        """
        Obtener la configuración del sitio usando el Singleton.
        """
        try:
            # Usar el método load() del Singleton
            config = SiteConfiguration.load()
            
            return JsonResponse({
                'site_name': config.site_name,
                'maintenance_mode': config.maintenance_mode,
                'default_max_exam_tries': config.default_max_exam_tries,
                'max_students_per_course': config.max_students_per_course,
                'enable_notifications': config.enable_notifications,
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    @method_decorator(csrf_exempt)
    def post(self, request):
        """
        Actualizar la configuración del sitio.
        """
        try:
            data = json.loads(request.body)
            config = SiteConfiguration.load()
            
            # Actualizar campos permitidos
            if 'site_name' in data:
                config.site_name = data['site_name']
            if 'maintenance_mode' in data:
                config.maintenance_mode = data['maintenance_mode']
            if 'default_max_exam_tries' in data:
                config.default_max_exam_tries = data['default_max_exam_tries']
            if 'max_students_per_course' in data:
                config.max_students_per_course = data['max_students_per_course']
            if 'enable_notifications' in data:
                config.enable_notifications = data['enable_notifications']
            
            config.save()
            
            return JsonResponse({'message': 'Configuración actualizada correctamente'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def health_check(request):
    """
    Verificación de salud del sistema usando el Singleton.
    """
    try:
        config = SiteConfiguration.load()
        
        return JsonResponse({
            'status': 'healthy',
            'maintenance_mode': config.maintenance_mode,
            'site_name': config.site_name
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e)
        }, status=500)