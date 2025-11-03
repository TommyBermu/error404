from django.contrib import admin

from accounts.models import AppUser

@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'role', 'status', 'created_at')
    list_filter = ('role', 'status')
    search_fields = ('email', 'first_name')
    
    # Permite editar el rol directamente
    fieldsets = (
        ('Información básica', {
            'fields': ('username', 'email', 'first_name', 'last_name')
        }),
        ('Permisos y rol', {
            'fields': ('role', 'status', 'is_staff', 'is_superuser', 'is_active')
        }),
        ('Fechas', {
            'fields': ('last_login', 'date_joined')
        }),
    )