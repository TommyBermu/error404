from django.db import models
from django.conf import settings

class Team(models.Model):
    """Equipos de trabajo"""
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True)
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='supervised_teams'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'team'
        verbose_name = 'Equipo'
        verbose_name_plural = 'Equipos'
    
    def __str__(self):
        return self.name


class TeamUser(models.Model):
    """Relación entre usuarios y equipos (membresía)"""
    app_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='team_memberships'
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='members'
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    role_in_team = models.CharField(max_length=50, blank=True)
    
    class Meta:
        db_table = 'team_user'
        verbose_name = 'Miembro de equipo'
        verbose_name_plural = 'Miembros de equipos'
        unique_together = ('app_user', 'team')
    
    def __str__(self):
        return f"{self.app_user} en {self.team}"