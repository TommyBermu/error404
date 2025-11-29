from accounts.models import AppUser
from learning_paths.models import LearningPath
from teams.models import TeamUser


def get_paths_for_user(user: AppUser):
    """
    Retorna las rutas accesibles usando únicamente PathInscription.
    """

    # 1. Analista TH → ve todas las rutas
    if user.role == AppUser.UserRole.ANALISTA_TH:
        return LearningPath.objects.all()

    # 2. Supervisor → rutas inscritas por su equipo
    if user.role == AppUser.UserRole.SUPERVISOR:
        return _get_paths_for_supervisor(user)

    # 3. Colaborador → rutas en las que él mismo está inscrito
    if user.role == AppUser.UserRole.COLABORADOR:
        return _get_paths_for_colaborador(user)

    return LearningPath.objects.none()


def _get_paths_for_colaborador(user: AppUser):
    """
    Rutas donde el colaborador esté inscrito.
    """
    return LearningPath.objects.filter(
        inscriptions__app_user=user
    ).distinct()


def _get_paths_for_supervisor(user: AppUser):
    """
    Rutas inscritas por miembros de su equipo.
    """

    # Usuarios del equipo del supervisor
    team_members_ids = TeamUser.objects.filter(
        team__supervisor=user
    ).values_list("app_user_id", flat=True)

    if not team_members_ids:
        return LearningPath.objects.none()

    return LearningPath.objects.filter(
        inscriptions__app_user_id__in=team_members_ids
    ).distinct()
