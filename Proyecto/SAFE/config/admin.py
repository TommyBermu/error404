# SAFE/config/admin.py
from django.contrib import admin
from .models import SiteConfiguration

@admin.register(SiteConfiguration)
class SiteConfigurationAdmin(admin.ModelAdmin):
    """
    Admin interface for SiteConfiguration singleton.
    """
    list_display = ['site_name', 'maintenance_mode', 'default_max_exam_tries', 'max_students_per_course', 'enable_notifications']
    list_editable = ['maintenance_mode', 'default_max_exam_tries', 'max_students_per_course', 'enable_notifications']
    
    def has_add_permission(self, request):
        """
        Prevent adding new instances (singleton behavior).
        """
        return False
    
    def has_delete_permission(self, request, obj=None):
        """
        Prevent deleting the singleton instance.
        """
        return False
    
    def get_queryset(self, request):
        """
        Always return the singleton instance.
        """
        return SiteConfiguration.objects.filter(pk=1)
    
    def changelist_view(self, request, extra_context=None):
        """
        Redirect to change view for the singleton instance.
        """
        obj = SiteConfiguration.get_config()
        return self.change_view(request, str(obj.pk), extra_context)
