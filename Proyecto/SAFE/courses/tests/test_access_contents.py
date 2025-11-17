from django.test import TestCase
from django.contrib.auth import get_user_model

from courses.models import Course, Module, Content
from enrollments.models import CourseInscription
from teams.models import Team, TeamUser
from courses.services.access import get_contents_for_user_in_course

User = get_user_model()


class GetContentsForUserTests(TestCase):

    def setUp(self):
        # Usuarios
        self.analista = User.objects.create_user(username="a", password="123", role="analistaTH", email="a123@gmail.com")
        self.supervisor = User.objects.create_user(username="s", password="123", role="supervisor", email="s123@gmail.com")
        self.colab = User.objects.create_user(username="c", password="123", role="colaborador", email="c123@gmail.com")

        # Equipo para supervisor
        self.team = Team.objects.create(name="T1", supervisor=self.supervisor)
        self.memberA = User.objects.create_user(username="mA", password="123", email="mA123@gmail.com")
        TeamUser.objects.create(app_user=self.memberA, team=self.team)

        # Curso y módulo
        self.course = Course.objects.create(name="Curso X", status=Course.CourseStatus.ACTIVE)
        self.mod = Module.objects.create(course=self.course, name="Módulo 1")

        # Contenidos secuenciales
        self.c1 = Content.objects.create(module=self.mod, title="C1", content_type="material")
        self.c2 = Content.objects.create(module=self.mod, title="C2", previous_content=self.c1, content_type="material")
        self.c3 = Content.objects.create(
            module=self.mod, title="C3", previous_content=self.c2,
            content_type="material", is_mandatory=True
        )
        self.c4 = Content.objects.create(
            module=self.mod, title="C4", previous_content=self.c3,
            content_type="material"
        )

    def test_analista_ve_todos_los_contenidos(self):
        contenidos = get_contents_for_user_in_course(self.analista, self.course)
        self.assertEqual(len(contenidos), 4)

    def test_supervisor_ve_contenidos_solo_si_su_equipo_esta_inscrito(self):
        # Inscribir solo al miembro, no al supervisor
        CourseInscription.objects.create(app_user=self.memberA, course=self.course)

        contenidos = get_contents_for_user_in_course(self.supervisor, self.course)
        self.assertEqual(len(contenidos), 4)

    def test_supervisor_sin_equipo_ni_inscripcion_no_ve_nada(self):
        supervisor2 = User.objects.create(username="s2", password="123", role="supervisor")
        contenidos = get_contents_for_user_in_course(supervisor2, self.course)
        self.assertEqual(len(contenidos), 0)

    def test_colaborador_ve_secuencia_hasta_contenido_mandatorio(self):
        CourseInscription.objects.create(app_user=self.colab, course=self.course)

        contenidos = get_contents_for_user_in_course(self.colab, self.course)
        # debe ver C1, C2, C3 y parar
        self.assertEqual([self.c1, self.c2, self.c3], list(contenidos))

    def test_colaborador_no_inscrito_no_ve_contenidos(self):
        contenidos = get_contents_for_user_in_course(self.colab, self.course)
        self.assertEqual(len(contenidos), 0)
