from django.db import models
from django.contrib.auth.models import AbstractUser

class AppUser(AbstractUser):
    """Usuario extendido con roles y estado"""
    
    class UserRole(models.TextChoices):
        COLABORADOR = 'colaborador', 'Colaborador'
        SUPERVISOR = 'supervisor', 'Supervisor'
        ANALISTA_TH = 'analistaTH', 'Analista TH'
    
    class UserStatus(models.TextChoices):
        ACTIVE = 'active', 'Activo'
        INACTIVE = 'inactive', 'Inactivo'
        PENDING = 'pending', 'Pendiente'
    
    # Sobrescribir campos heredados
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, verbose_name='name')
    last_name = models.CharField(max_length=100, verbose_name='last name')
    password = models.CharField(max_length=128, verbose_name='password')
    
    
    # Campos personalizados
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=UserStatus.choices,
        default=UserStatus.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # last_login ya viene en AbstractUser
    
    class Meta:
        db_table = 'app_user'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.first_name} ({self.email})"
    
class RoleChangeLog(models.Model):
    """Registro histórico de cambios de rol"""

    changed_by = models.ForeignKey(
        'accounts.AppUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='role_changes_made'
    )
    target_user = models.ForeignKey(
        'accounts.AppUser',
        on_delete=models.CASCADE,
        related_name='role_changes_received'
    )
    old_role = models.CharField(
        max_length=20,
        null=True,
        blank=True
    )
    new_role = models.CharField(max_length=20)
    changed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'role_change_log'
        verbose_name = "Cambio de Rol"
        verbose_name_plural = "Cambios de Rol"

    def __str__(self):
        return f"{self.changed_by} cambió {self.target_user} de {self.old_role} a {self.new_role}"
