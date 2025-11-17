from django.test import TestCase
from django.contrib.auth import get_user_model

from courses.models import Course
from learning_paths.models import LearningPath, CourseInPath
from enrollments.models import CourseInscription
from teams.models import Team, TeamUser
from courses.services.access import get_courses_in_learning_path_for_user

User = get_user_model()


class GetCoursesInPathTests(TestCase):

    def setUp(self):
        # Usuarios
        self.analista = User.objects.create_user(username="a", password="123", role="analistaTH", email="a123@gmail.com")
        self.supervisor = User.objects.create_user(username="s", password="123", role="supervisor", email="s123@gmail.com")
        self.colab = User.objects.create_user(username="c", password="123", role="colaborador", email="c123@gmail.com")

        # Equipo
        self.team = Team.objects.create(name="Team A", supervisor=self.supervisor)
        self.memberA = User.objects.create_user(username="mA", password="123", email="mA123@gmail.com")
        TeamUser.objects.create(app_user=self.memberA, team=self.team)

        # Cursos y ruta
        self.course1 = Course.objects.create(name="C1", status=Course.CourseStatus.ACTIVE)
        self.course2 = Course.objects.create(name="C2", status=Course.CourseStatus.ACTIVE)
        self.path = LearningPath.objects.create(name="Ruta X")

        CourseInPath.objects.create(learning_path=self.path, course=self.course1)
        CourseInPath.objects.create(learning_path=self.path, course=self.course2)

    def test_analista_ve_todos_los_cursos_de_la_ruta(self):
        cursos = get_courses_in_learning_path_for_user(self.analista, self.path)
        self.assertEqual(set(cursos), {self.course1, self.course2})

    def test_supervisor_ve_cursos_con_inscripcion_de_equipo(self):
        CourseInscription.objects.create(app_user=self.memberA, course=self.course1)

        cursos = get_courses_in_learning_path_for_user(self.supervisor, self.path)

        self.assertEqual(list(cursos), [self.course1])

    def test_supervisor_sin_equipo_inscrito_no_ve_cursos(self):
        cursos = get_courses_in_learning_path_for_user(self.supervisor, self.path)
        self.assertEqual(len(cursos), 0)

    def test_colaborador_ve_solo_sus_cursos_en_la_ruta(self):
        CourseInscription.objects.create(app_user=self.colab, course=self.course2)

        cursos = get_courses_in_learning_path_for_user(self.colab, self.path)

        self.assertEqual(list(cursos), [self.course2])

    def test_colaborador_sin_inscripcion_no_ve_nada(self):
        cursos = get_courses_in_learning_path_for_user(self.colab, self.path)
        self.assertEqual(len(cursos), 0)
