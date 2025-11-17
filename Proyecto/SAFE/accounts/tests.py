from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import AppUser
from accounts.views import unique_email
import unittest

'''
Crear una función llamada “unique_email” que valide si un email es único en la base de datos.:
    El email debe ser único en la tabla de usuarios.
    La función debe recibir un email como parámetro y retornar True si es único, False en caso contrario.

Generar los test.
'''

User = get_user_model()
class UniqueEmailTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Creamos un usuario que SÍ existe
        cls.user = User.objects.create(
            username="testuser",
            email="existe@safe.com"
        )

    def test_unique_email_true(self):
        """Debe retornar True cuando el email existe."""
        result = unique_email("existe@safe.com")
        self.assertTrue(result)

    def test_unique_email_false(self):
        """Debe retornar False cuando el email NO existe."""
        result = unique_email("noexiste@safe.com")
        self.assertFalse(result)



if __name__ == '__main__':
    unittest.main()
