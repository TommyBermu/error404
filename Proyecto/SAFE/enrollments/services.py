from accounts.models import AppUser
from courses.models import Course, Content
from enrollments.models import CourseInscription
from learning_paths.models import LearningPath
from teams.models import TeamUser


def get_courses_for_user(user: AppUser):
    """
    Return the courses visible to a user according to their role.
    """

    # 1. Analista TH -> all active courses
    if user.role == AppUser.UserRole.ANALISTA_TH:
        return Course.objects.filter(status=Course.CourseStatus.ACTIVE)

    # 2. Supervisor -> courses where someone in their team is enrolled
    if user.role == AppUser.UserRole.SUPERVISOR:
        team_members = TeamUser.objects.filter(
            team__supervisor=user
        ).values_list("app_user_id", flat=True)

        if not team_members:
            return Course.objects.none()

        return (
            Course.objects.filter(
                inscriptions__app_user_id__in=team_members,
                status=Course.CourseStatus.ACTIVE,
            )
            .distinct()
        )

    # 3. Colaborador -> own courses
    if user.role == AppUser.UserRole.COLABORADOR:
        return (
            Course.objects.filter(
                inscriptions__app_user=user,
                status=Course.CourseStatus.ACTIVE,
            )
            .distinct()
        )

    return Course.objects.none()


def get_contents_for_user_in_course(user: AppUser, course: Course):
    """
    Determine which contents are visible for a given user inside a course.
    """

    # 1. Analista TH: can see everything
    if user.role == AppUser.UserRole.ANALISTA_TH:
        return Content.objects.filter(module__course=course)

    # 2. Supervisor: can see everything only if their team is enrolled
    if user.role == AppUser.UserRole.SUPERVISOR:
        team_members = TeamUser.objects.filter(
            team__supervisor=user
        ).values_list("app_user_id", flat=True)

        if CourseInscription.objects.filter(
            app_user_id__in=team_members, course=course
        ).exists():
            return Content.objects.filter(module__course=course)

        return Content.objects.none()

    # 3. Colaborador: sequential navigation based on course contents
    if user.role == AppUser.UserRole.COLABORADOR:
        if not CourseInscription.objects.filter(app_user=user, course=course).exists():
            return Content.objects.none()

        all_contents = Content.objects.filter(module__course=course)

        visible_contents = []
        current = all_contents.filter(previous_content__isnull=True).first()

        # traverse the sequence until a mandatory content is reached
        while current:
            visible_contents.append(current)
            if current.is_mandatory:
                break
            current = all_contents.filter(previous_content=current).first()

        return visible_contents

    return Content.objects.none()


def get_courses_in_learning_path_for_user(user: AppUser, path: LearningPath):
    """
    Return the courses inside a learning path that are visible for the user.
    """

    # 1. Analista TH -> all active courses inside the path
    if user.role == AppUser.UserRole.ANALISTA_TH:
        return Course.objects.filter(
            in_paths__learning_path=path, status=Course.CourseStatus.ACTIVE
        ).distinct()

    # 2. Supervisor -> courses in the path where their team is enrolled
    if user.role == AppUser.UserRole.SUPERVISOR:
        team_members = TeamUser.objects.filter(
            team__supervisor=user
        ).values_list("app_user_id", flat=True)

        if not team_members:
            return Course.objects.none()

        return (
            Course.objects.filter(
                in_paths__learning_path=path,
                inscriptions__app_user_id__in=team_members,
                status=Course.CourseStatus.ACTIVE,
            )
            .distinct()
        )

    # 3. Colaborador -> courses in the path where they are enrolled
    if user.role == AppUser.UserRole.COLABORADOR:
        return (
            Course.objects.filter(
                in_paths__learning_path=path,
                inscriptions__app_user=user,
                status=Course.CourseStatus.ACTIVE,
            )
            .distinct()
        )

    return Course.objects.none()


def get_paths_for_user(user: AppUser):
    """
    Return the learning paths visible to the user using only PathInscription.
    """

    # 1. Analista TH -> all paths
    if user.role == AppUser.UserRole.ANALISTA_TH:
        return LearningPath.objects.all()

    # 2. Supervisor -> paths where their team is enrolled
    if user.role == AppUser.UserRole.SUPERVISOR:
        return _get_paths_for_supervisor(user)

    # 3. Colaborador -> paths where they are enrolled
    if user.role == AppUser.UserRole.COLABORADOR:
        return _get_paths_for_colaborador(user)

    return LearningPath.objects.none()


def _get_paths_for_colaborador(user: AppUser):
    """Helper: paths where the collaborator is enrolled."""
    return LearningPath.objects.filter(inscriptions__app_user=user).distinct()


def _get_paths_for_supervisor(user: AppUser):
    """Helper: paths where someone in the supervisor's team is enrolled."""
    team_members_ids = TeamUser.objects.filter(
        team__supervisor=user
    ).values_list("app_user_id", flat=True)

    if not team_members_ids:
        return LearningPath.objects.none()

    return LearningPath.objects.filter(
        inscriptions__app_user_id__in=team_members_ids
    ).distinct()
