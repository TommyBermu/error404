from django.test import TestCase
from django.core.exceptions import PermissionDenied
from accounts.models import AppUser, RoleChangeLog
from accounts.services import change_role

class ChangeRoleTests(TestCase):

    def setUp(self):
        self.analista = AppUser.objects.create_user(
            username="ana",
            password="123",
            role="analistaTH",
            email="ana123@gmail.com"
        )

        self.colaborador = AppUser.objects.create_user(
            username="carlos",
            password="123",
            role="colaborador",
            email="carlos123@gmail.com"
        )

        self.user_sin_rol = AppUser.objects.create_user(
            username="nulo",
            password="123",
            role=None,
            email="nulo@gmail.com"
        )

    def test_change_role_retorna_true(self):
        result = change_role(self.analista, self.colaborador, "supervisor")
        self.assertTrue(result)

    def test_no_se_puede_asignar_rol_invalido(self):
        with self.assertRaises(ValueError):
            change_role(self.analista, self.colaborador, "jefeSupremo")

    def test_no_se_puede_asignar_rol_nulo(self):
        with self.assertRaises(ValueError):
            change_role(self.analista, self.colaborador, None)
    
    def test_cambiar_por_el_mismo_rol_generates_log(self):
        change_role(self.analista, self.colaborador, "colaborador")

        logs = RoleChangeLog.objects.all()
        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs.first().old_role, "colaborador")
        self.assertEqual(logs.first().new_role, "colaborador")
    
    def test_analista_no_puede_cambiar_su_propio_rol(self):
        with self.assertRaises(PermissionDenied):
            change_role(self.analista, self.analista, "supervisor")

    def test_usuario_sin_rol_previene_rol_nuevo(self):
        change_role(self.analista, self.user_sin_rol, "supervisor")
        self.user_sin_rol.refresh_from_db()

        self.assertEqual(self.user_sin_rol.role, "supervisor")

    def test_analista_puede_cambiar_rol(self):
        change_role(self.analista, self.colaborador, "supervisor")
        self.colaborador.refresh_from_db()
        self.assertEqual(self.colaborador.role, "supervisor")

    def test_no_analista_no_puede_cambiar_rol(self):
        with self.assertRaises(PermissionDenied):
            change_role(self.colaborador, self.analista, "supervisor")

    def test_registro_de_bitacora(self):
        change_role(self.analista, self.colaborador, "supervisor")
        log = RoleChangeLog.objects.first()

        self.assertIsNotNone(log)
        self.assertEqual(log.old_role, "colaborador")
        self.assertEqual(log.new_role, "supervisor")
        self.assertEqual(log.changed_by, self.analista)
        self.assertEqual(log.target_user, self.colaborador)

    def test_multiples_cambios_generan_multiples_logs(self):
        change_role(self.analista, self.colaborador, "supervisor")
        change_role(self.analista, self.colaborador, "analistaTH")

        logs = RoleChangeLog.objects.filter(target_user=self.colaborador)

        self.assertEqual(logs.count(), 2)
        self.assertEqual(logs.first().old_role, "colaborador")
        self.assertEqual(logs.last().new_role, "analistaTH")

