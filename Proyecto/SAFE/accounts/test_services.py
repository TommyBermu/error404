from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import AppUser
from accounts.services import change_role

User = get_user_model()


class ChangeRoleServiceTests(TestCase):
    def setUp(self):
        self.analyst = User.objects.create_user(
            username="analyst",
            email="analyst@example.com",
            password="password123",
            first_name="Ana",
            last_name="Lista",
            role=AppUser.UserRole.ANALISTA_TH,
        )
        self.supervisor = User.objects.create_user(
            username="supervisor",
            email="supervisor@example.com",
            password="password123",
            first_name="Sue",
            last_name="Pervisora",
            role=AppUser.UserRole.SUPERVISOR,
        )
        self.collaborator = User.objects.create_user(
            username="collaborator",
            email="collaborator@example.com",
            password="password123",
            first_name="Cole",
            last_name="Laborador",
            role=AppUser.UserRole.COLABORADOR,
        )

    def test_permission_denied_for_non_analyst(self):
        result = change_role(
            actor=self.supervisor,
            target=self.collaborator,
            new_role=AppUser.UserRole.ANALISTA_TH,
        )

        self.assertFalse(result)
        self.collaborator.refresh_from_db()
        self.assertEqual(self.collaborator.role, AppUser.UserRole.COLABORADOR)

    def test_invalid_role_is_rejected(self):
        result = change_role(
            actor=self.analyst,
            target=self.collaborator,
            new_role="invalid_role",
        )

        self.assertFalse(result)
        self.collaborator.refresh_from_db()
        self.assertEqual(self.collaborator.role, AppUser.UserRole.COLABORADOR)

    def test_self_role_change_is_blocked(self):
        result = change_role(
            actor=self.analyst,
            target=self.analyst,
            new_role=AppUser.UserRole.SUPERVISOR,
        )

        self.assertFalse(result)
        self.analyst.refresh_from_db()
        self.assertEqual(self.analyst.role, AppUser.UserRole.ANALISTA_TH)

    def test_successful_role_update(self):
        result = change_role(
            actor=self.analyst,
            target=self.collaborator,
            new_role=AppUser.UserRole.SUPERVISOR,
        )

        self.assertTrue(result)
        self.collaborator.refresh_from_db()
        self.assertEqual(self.collaborator.role, AppUser.UserRole.SUPERVISOR)
