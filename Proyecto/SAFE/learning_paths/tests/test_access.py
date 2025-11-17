from django.test import TestCase
from django.contrib.auth import get_user_model

from learning_paths.models import LearningPath
from teams.models import Team, TeamUser
from enrollments.models import PathInscription
from learning_paths.services.access import get_paths_for_user

User = get_user_model()


class LearningPathAccessTests(TestCase):

    def setUp(self):
        # Usuarios
        self.colab = User.objects.create_user(
            username="colab", password="123",
            role="colaborador", email="colab@test.com"
        )

        self.supervisor = User.objects.create_user(
            username="sup", password="123",
            role="supervisor", email="super@test.com"
        )

        self.analista = User.objects.create_user(
            username="ana", password="123",
            role="analistaTH", email="ana@test.com"
        )

        # Rutas
        self.path1 = LearningPath.objects.create(name="Ruta 1")
        self.path2 = LearningPath.objects.create(name="Ruta 2")

        # Equipo a cargo del supervisor
        self.team = Team.objects.create(name="Equipo A", supervisor=self.supervisor)

        self.member1 = User.objects.create_user(
            username="m1", password="123", email="m1@test.com", role="colaborador"
        )

        self.member2 = User.objects.create_user(
            username="m2", password="123", email="m2@test.com", role="colaborador"
        )

        TeamUser.objects.create(app_user=self.member1, team=self.team)
        TeamUser.objects.create(app_user=self.member2, team=self.team)

    # ---------------------------------------------------------------------
    #          COLABORADOR
    # ---------------------------------------------------------------------

    def test_colaborador_accede_a_sus_rutas(self):
        PathInscription.objects.create(app_user=self.colab, learning_path=self.path1)

        rutas = get_paths_for_user(self.colab)

        self.assertEqual(len(rutas), 1)
        self.assertIn(self.path1, rutas)

    def test_colaborador_sin_inscripciones_no_ve_rutas(self):
        rutas = get_paths_for_user(self.colab)
        self.assertEqual(len(rutas), 0)

    def test_colaborador_no_ve_rutas_en_las_que_no_esta_inscrito(self):
        PathInscription.objects.create(app_user=self.colab, learning_path=self.path1)

        rutas = get_paths_for_user(self.colab)

        self.assertNotIn(self.path2, rutas)

    def test_colaborador_no_recibe_duplicados(self):
        PathInscription.objects.get_or_create(app_user=self.colab, learning_path=self.path1)
        PathInscription.objects.get_or_create(app_user=self.colab, learning_path=self.path1)

        rutas = get_paths_for_user(self.colab)

        self.assertEqual(len(rutas), 1)
        self.assertIn(self.path1, rutas)


    # ---------------------------------------------------------------------
    #          SUPERVISOR
    # ---------------------------------------------------------------------

    def test_supervisor_accede_a_rutas_de_su_equipo(self):
        PathInscription.objects.create(app_user=self.member1, learning_path=self.path1)

        rutas = get_paths_for_user(self.supervisor)

        self.assertEqual(len(rutas), 1)
        self.assertIn(self.path1, rutas)

    def test_supervisor_sin_miembros_no_accede_a_rutas(self):
        supervisor2 = User.objects.create_user(
            username="sup2", password="123", role="supervisor", email="s2@test.com"
        )

        rutas = get_paths_for_user(supervisor2)

        self.assertEqual(len(rutas), 0)

    def test_supervisor_ve_rutas_de_cualquier_miembro(self):
        PathInscription.objects.create(app_user=self.member2, learning_path=self.path2)

        rutas = get_paths_for_user(self.supervisor)

        self.assertEqual(len(rutas), 1)
        self.assertIn(self.path2, rutas)

    def test_supervisor_no_ve_rutas_si_nadie_en_su_equipo_inscribe(self):
        rutas = get_paths_for_user(self.supervisor)
        self.assertEqual(len(rutas), 0)

    # ---------------------------------------------------------------------
    #          ANALISTA
    # ---------------------------------------------------------------------

    def test_analista_ve_todas_las_rutas(self):
        # Crea inscripciones varias
        PathInscription.objects.create(app_user=self.colab, learning_path=self.path1)
        PathInscription.objects.create(app_user=self.member1, learning_path=self.path2)

        rutas = get_paths_for_user(self.analista)

        self.assertEqual(len(rutas), 2)
        self.assertIn(self.path1, rutas)
        self.assertIn(self.path2, rutas)
