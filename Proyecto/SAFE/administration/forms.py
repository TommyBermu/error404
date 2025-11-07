from django import forms
from courses.models import Course, Module, Content, Material, Exam, Assignment


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ["name", "description", "duration_hours", "status", "header_img"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-200 rounded-lg px-3 py-2",
                    "placeholder": "Nombre del curso",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full border border-gray-200 rounded-lg px-3 py-2 h-24",
                    "placeholder": "Descipción del curso",
                }
            ),
            "duration_hours": forms.NumberInput(
                attrs={"class": "w-full border border-gray-200 rounded-lg px-3 py-2"}
            ),
            "status": forms.Select(
                attrs={"class": "w-full border border-gray-200 rounded-lg px-3 py-2"}
            ),
        }
        labels = {
            "name": "Título del curso",
            "description": "Descripción",
            "duration_hours": "Duración (horas)",
            "status": "Estado",
            "header_img": "Imagen de portada",
        }


class ModuleForm(forms.ModelForm):
    class Meta:
        model = Module
        fields = ["name", "description", "duration_hours"]
        widgets = {
            "name": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-200 rounded-lg px-3 py-2",
                    "placeholder": "Nombre del módulo",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full border border-gray-200 rounded-lg px-3 py-2 h-20",
                    "placeholder": "Descripción del módulo",
                }
            ),
            "duration_hours": forms.NumberInput(
                attrs={"class": "w-full border border-gray-200 rounded-lg px-3 py-2"}
            ),
        }


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = ["title", "description", "content_type", "is_mandatory"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full border border-gray-200 rounded-lg px-3 py-2",
                    "placeholder": "Título del contenido",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "w-full border border-gray-200 rounded-lg px-3 py-2 h-20",
                    "placeholder": "Descripción",
                }
            ),
            "content_type": forms.Select(
                attrs={"class": "w-full border border-gray-200 rounded-lg px-3 py-2"}
            ),
            "is_mandatory": forms.CheckboxInput(attrs={"class": "rounded"}),
        }


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["type", "file"]
        widgets = {
            "type": forms.Select(
                attrs={"class": "w-full border border-gray-200 rounded-lg px-3 py-2"}
            ),
        }
