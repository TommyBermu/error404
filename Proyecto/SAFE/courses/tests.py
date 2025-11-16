# Create your tests here.
from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .forms import QuestionUploadForm
from .models import Course


class TestsQuestionUploadForm(TestCase):    
    @classmethod
    def setUpTestData(cls):
        cls.test_course = Course.objects.create(
            name="Test Course",
            description="A test course for form validation"
        )

    def test_upload_valid_txt_file(self):
        file_content = b"Contenido de prueba para el examen."
        file = SimpleUploadedFile(
            "preguntas.txt",
            file_content, 
            content_type="text/plain"
        )
        form_data = {
            'course': self.test_course.id,
            'difficulty': 'media'
        }
        file_data = {'file': file}

        form = QuestionUploadForm(form_data, file_data)

        self.assertTrue(form.is_valid(), f"El formulario debería ser válido. Errores: {form.errors}")

    def test_reject_invalid_extension_file(self):
        
        file_content = b"Esto es una imagen, no texto."
        file = SimpleUploadedFile(
            "imagen.png", 
            file_content, 
            content_type="image/png"
        )
        
        form_data = {
            'course': self.test_course.id,
            'difficulty': 'media'
        }
        file_data = {'file': file}

        form = QuestionUploadForm(form_data, file_data)

        self.assertFalse(form.is_valid(), "El formulario debería ser inválido por la extensión.")
        
        self.assertIn('file', form.errors, "Debería haber un error en el campo 'file'.")
        self.assertTrue(
            any("Solo se permiten archivos con extensión .txt" in str(error) 
                for error in form.errors['file']),
            f"Expected error message not found. Got: {form.errors['file']}"
        )

    def test_form_is_invalid_if_no_file_is_sent(self):
        
        form_data = {
            'course': self.test_course.id,
            'difficulty': 'media'
        }
        file_data = {}

        form = QuestionUploadForm(form_data, file_data)

        self.assertFalse(form.is_valid(), "El formulario no debe ser válido si no se envía un archivo.")
        self.assertIn('file', form.errors, "Debería reportar un error en 'file'.")
        
    def test_form_is_invalid_if_no_course_selected(self):

        file_content = b"Contenido de prueba."
        file = SimpleUploadedFile(
            "preguntas.txt",
            file_content, 
            content_type="text/plain"
        )
        form_data = {
            'difficulty': 'media'
        }
        file_data = {'file': file}

        form = QuestionUploadForm(form_data, file_data)

        self.assertFalse(form.is_valid(), "El formulario no debe ser válido sin seleccionar curso.")
        self.assertIn('course', form.errors, "Debería reportar un error en 'course'.")
        
    def test_form_is_invalid_if_no_difficulty_selected(self):
        file_content = b"Contenido de prueba."
        file = SimpleUploadedFile(
            "preguntas.txt",
            file_content, 
            content_type="text/plain"
        )
        form_data = {
            'course': self.test_course.id
        }
        file_data = {'file': file}

        form = QuestionUploadForm(form_data, file_data)

        self.assertFalse(form.is_valid(), "El formulario no debe ser válido sin seleccionar dificultad.")
        self.assertIn('difficulty', form.errors, "Debería reportar un error en 'difficulty'.")
