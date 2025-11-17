from accounts.models import AppUser
from courses.models import Course, Content
from enrollments.models import CourseInscription
from learning_paths.models import LearningPath, CourseInPath
from teams.models import TeamUser

def get_courses_for_user(user: AppUser):
    """
    Cursos visibles para el usuario según su rol.
    """

    # 1. Analista TH → ve todos los cursos activos
    if user.role == AppUser.UserRole.ANALISTA_TH:
        return Course.objects.filter(status=Course.CourseStatus.ACTIVE)

    # 2. Supervisor → cursos donde su equipo esté inscrito
    if user.role == AppUser.UserRole.SUPERVISOR:
        team_members = TeamUser.objects.filter(team__supervisor=user)\
                                       .values_list('app_user_id', flat=True)

        if not team_members:
            return Course.objects.none()

        return Course.objects.filter(
            inscriptions__app_user_id__in=team_members,
            status=Course.CourseStatus.ACTIVE
        ).distinct()

    # 3. Colaborador → cursos propios
    if user.role == AppUser.UserRole.COLABORADOR:
        return Course.objects.filter(
            inscriptions__app_user=user,
            status=Course.CourseStatus.ACTIVE
        ).distinct()

    return Course.objects.none()




def get_contents_for_user_in_course(user: AppUser, course: Course):
    """
    Determina los contenidos visibles para un usuario dentro de un curso.
    """

    # 1. Analista TH: ve todo
    if user.role == AppUser.UserRole.ANALISTA_TH:
        return Content.objects.filter(module__course=course)

    # 2. Supervisor: ve todo, pero solo si su equipo está inscrito
    if user.role == AppUser.UserRole.SUPERVISOR:
        from teams.models import TeamUser

        team_members = TeamUser.objects.filter(team__supervisor=user)\
                                       .values_list('app_user_id', flat=True)

        if CourseInscription.objects.filter(app_user_id__in=team_members, course=course).exists():
            return Content.objects.filter(module__course=course)

        return Content.objects.none()

    # 3. Colaborador: navegación secuencial
    if user.role == AppUser.UserRole.COLABORADOR:

        # Verifica inscripción
        if not CourseInscription.objects.filter(app_user=user, course=course).exists():
            return Content.objects.none()

        # Se trae los contenidos ordenados por secuencia
        all_contents = Content.objects.filter(module__course=course)

        visibles = []
        current = all_contents.filter(previous_content__isnull=True).first()

        # Recorre la lista secuencial
        while current:
            visibles.append(current)
            if current.is_mandatory:
                break
            current = all_contents.filter(previous_content=current).first()

        return visibles

    return Content.objects.none()




def get_courses_in_learning_path_for_user(user: AppUser, path: LearningPath):
    """
    Retorna los cursos visibles dentro de una ruta de aprendizaje,
    según el rol del usuario.
    """

    # 1. Analista TH → ve todos los cursos activos en la ruta
    if user.role == AppUser.UserRole.ANALISTA_TH:
        return Course.objects.filter(
            in_paths__learning_path=path,
            status=Course.CourseStatus.ACTIVE
        ).distinct()

    # 2. Supervisor → cursos dentro de la ruta en los que su equipo esté inscrito
    if user.role == AppUser.UserRole.SUPERVISOR:
        team_members = TeamUser.objects.filter(
            team__supervisor=user
        ).values_list("app_user_id", flat=True)

        if not team_members:
            return Course.objects.none()

        # Cursos del path donde haya inscripción del equipo
        return Course.objects.filter(
            in_paths__learning_path=path,
            inscriptions__app_user_id__in=team_members,
            status=Course.CourseStatus.ACTIVE
        ).distinct()

    # 3. Colaborador → cursos del path en los que él mismo esté inscrito
    if user.role == AppUser.UserRole.COLABORADOR:
        return Course.objects.filter(
            in_paths__learning_path=path,
            inscriptions__app_user=user,
            status=Course.CourseStatus.ACTIVE
        ).distinct()

    # Rol no reconocido
    return Course.objects.none()
