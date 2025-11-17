from django import forms
from courses.models import Course, Module, Content, Material, Exam, Assignment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "description", "duration_hours", "status", "header_img"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full",
                    "placeholder": "Título del curso",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "placeholder": "Descripción del curso",
                    "rows": 4,
                }
            ),
            "duration_hours": forms.NumberInput(
                attrs={
                    "class": "",
                    "min": 0,
                }
            ),
            "status": forms.Select(attrs={"class": ""}),
        }
        labels = {
            "name": "Título del curso",
            "description": "Descripción",
            "duration_hours": "Duración (horas)",
            "status": "Estado",
            "header_img": "Imagen de portada",
        }

    def clean_duration_hours(self):
        """Valida que la duración no sea negativa."""
        duration = self.cleaned_data.get("duration_hours")
        if duration is not None and duration < 0:
            raise forms.ValidationError("La duración no puede ser negativa.")
        return duration


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ["name", "description", "duration_hours"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "inline-input w-full",
                    "placeholder": "Nombre del nuevo módulo",
                    "style": "padding:12px;border-radius:8px;border:1px solid var(--safe-border);",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "placeholder": "Descripción del módulo (opcional)",
                    "rows": 3,
                }
            ),
            "duration_hours": forms.NumberInput(
                attrs={
                    "class": "",
                    "min": 0,
                }
            ),
        }
        labels = {
            "name": "Nombre",
            "description": "Descripción",
            "duration_hours": "Duración (horas)",
        }


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ["title", "description", "block_type", "is_mandatory"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full",
                    "placeholder": "Título del contenido",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full",
                    "placeholder": "Descripción breve del contenido",
                    "rows": 4,
                }
            ),
            "block_type": forms.Select(
                attrs={
                    "class": "w-full",
                }
            ),
            "is_mandatory": forms.CheckboxInput(
                attrs={
                    "class": "checkbox-input",
                }
            ),
        }
        labels = {
            "title": "Título",
            "description": "Descripción",
            "block_type": "Tipo de bloque",
            "is_mandatory": "Contenido obligatorio",
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["type", "file"]
        widgets = {
            "type": forms.Select(attrs={"class": ""}),
            "file": forms.FileInput(attrs={"class": ""}),
        }
        labels = {
            "type": "Tipo de archivo",
            "file": "Archivo",
        }
