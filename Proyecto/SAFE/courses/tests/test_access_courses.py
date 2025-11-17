from django.test import TestCase
from django.contrib.auth import get_user_model

from courses.models import Course
from enrollments.models import CourseInscription
from teams.models import Team, TeamUser
from courses.services.access import get_courses_for_user

User = get_user_model()

class GetCoursesForUserTests(TestCase):

    def setUp(self):
        # Usuarios
        self.analista = User.objects.create_user(username="a", password="123", role="analistaTH", email="a123@gmail.com")
        self.supervisor = User.objects.create_user(username="s", password="123", role="supervisor", email="s123@gmail.com")
        self.colab = User.objects.create_user(username="c", password="123", role="colaborador", email="c123@gmail.com")

        # Equipo del supervisor
        self.team = Team.objects.create(name="Team A", supervisor=self.supervisor)
        self.memberA = User.objects.create_user(username="mA", password="123", email="mA123@gmail.com")
        TeamUser.objects.create(app_user=self.memberA, team=self.team)

        # Cursos
        self.course_active = Course.objects.create(
            name="Curso Activo",
            status=Course.CourseStatus.ACTIVE
        )
        self.course_draft = Course.objects.create(
            name="Curso Borrador",
            status=Course.CourseStatus.DRAFT
        )

    def test_analista_ve_todos_los_cursos_activos(self):
        cursos = get_courses_for_user(self.analista)
        self.assertIn(self.course_active, cursos)
        self.assertNotIn(self.course_draft, cursos)

    def test_supervisor_ve_cursos_de_equipo(self):
        CourseInscription.objects.create(
            app_user=self.memberA,
            course=self.course_active
        )

        cursos = get_courses_for_user(self.supervisor)

        self.assertEqual(list(cursos), [self.course_active])

    def test_supervisor_sin_equipo_no_ve_cursos(self):
        supervisor2 = User.objects.create(
            username="sup2", password="123", role="supervisor"
        )

        cursos = get_courses_for_user(supervisor2)
        self.assertEqual(len(cursos), 0)

    def test_colaborador_ve_solo_sus_cursos(self):
        CourseInscription.objects.create(app_user=self.colab, course=self.course_active)

        cursos = get_courses_for_user(self.colab)

        self.assertEqual(list(cursos), [self.course_active])

    def test_colaborador_sin_inscripcion_no_ve_nada(self):
        cursos = get_courses_for_user(self.colab)
        self.assertEqual(len(cursos), 0)
