from django.db import models
from django.conf import settings

class Course(models.Model):
    """Cursos de formación"""
    
    class CourseStatus(models.TextChoices):
        ACTIVE = 'active', 'Activo'
        DRAFT = 'draft', 'Borrador'
        ARCHIVED = 'archived', 'Archivado'
    
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    duration_hours = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_courses'
    )
    header_img = models.BinaryField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=CourseStatus.choices,
        default=CourseStatus.DRAFT
    )
    
    class Meta:
        db_table = 'course'
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
    
    def __str__(self):
        return self.name


class Module(models.Model):
    """Módulos dentro de un curso"""
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='modules'
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    previous_module = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_modules'
    )
    next_module = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='previous_modules'
    )
    duration_hours = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'module'
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
    
    def __str__(self):
        return f"{self.course.name} - {self.name}"


class Exam(models.Model):
    """Exámenes"""
    total_questions = models.IntegerField(null=True, blank=True)
    passing_score = models.IntegerField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    max_tries = models.IntegerField(null=True, blank=True)
    questions = models.JSONField(null=True, blank=True)
    
    class Meta:
        db_table = 'exam'
        verbose_name = 'Examen'
        verbose_name_plural = 'Exámenes'


class Assignment(models.Model):
    """Tareas/Asignaciones"""
    
    class MaterialType(models.TextChoices):
        MP4 = 'mp4', 'Video MP4'
        MP3 = 'mp3', 'Audio MP3'
        JPG = 'jpg', 'Imagen JPG'
        PDF = 'pdf', 'Documento PDF'
        TXT = 'txt', 'Texto plano'
    
    type = models.CharField(
        max_length=10,
        choices=MaterialType.choices,
        null=True,
        blank=True
    )
    max_score = models.IntegerField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'assignment'
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'


class Material(models.Model):
    """Materiales de aprendizaje"""
    
    class MaterialType(models.TextChoices):
        MP4 = 'mp4', 'Video MP4'
        MP3 = 'mp3', 'Audio MP3'
        JPG = 'jpg', 'Imagen JPG'
        PDF = 'pdf', 'Documento PDF'
        TXT = 'txt', 'Texto plano'
    
    type = models.CharField(
        max_length=10,
        choices=MaterialType.choices,
        null=True,
        blank=True
    )
    file = models.BinaryField(null=True, blank=True)
    
    class Meta:
        db_table = 'material'
        verbose_name = 'Material'
        verbose_name_plural = 'Materiales'


class Content(models.Model):
    """Contenido polimórfico (exam, assignment, material)"""
    
    class ContentType(models.TextChoices):
        EXAM = 'exam', 'Examen'
        ASSIGNMENT = 'assignment', 'Tarea'
        MATERIAL = 'material', 'Material'
    
    module = models.ForeignKey(
        Module,
        on_delete=models.CASCADE,
        related_name='contents'
    )
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    content_type = models.CharField(
        max_length=20,
        choices=ContentType.choices
    )
    
    # Relación polimórfica
    exam = models.ForeignKey(
        Exam,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contents'
    )
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contents'
    )
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='contents'
    )
    
    # Orden secuencial
    previous_content = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='next_contents'
    )
    next_content = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='previous_contents'
    )
    
    is_mandatory = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'content'
        verbose_name = 'Contenido'
        verbose_name_plural = 'Contenidos'
    
    def __str__(self):
        return f"{self.title} ({self.content_type})"