# SAFE/config/models.py
from django.db import models
from core.models import SingletonModel

class SiteConfiguration(SingletonModel):
    """
    Singleton model to store global settings for the
    SAFE e-learning platform.
    """
    site_name = models.CharField(
        max_length=150, 
        default='Plataforma de Aprendizaje SAFE',
        help_text="Nombre de la plataforma de aprendizaje"
    )
    
    maintenance_mode = models.BooleanField(
        default=False,
        help_text="Activar modo de mantenimiento del sitio"
    )
    
    default_max_exam_tries = models.PositiveSmallIntegerField(
        default=3,
        help_text="Número máximo de intentos por defecto para un examen"
    )
    
    max_students_per_course = models.PositiveIntegerField(
        default=50,
        help_text="Número máximo de estudiantes por curso"
    )
    
    enable_notifications = models.BooleanField(
        default=True,
        help_text="Activar sistema de notificaciones"
    )

    def __str__(self):
        return f"Configuración Global de SAFE - {self.site_name}"

    class Meta:
        verbose_name = "Configuración Global del Sitio"
        verbose_name_plural = "Configuraciones Globales del Sitio"
        
    @classmethod
    def get_config(cls):
        """
        Método de conveniencia para obtener la configuración del sitio.
        """
        return cls.load()