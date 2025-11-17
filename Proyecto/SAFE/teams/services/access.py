# teams/services/access.py

from teams.models import Team


def supervisor_has_team(user):
    """
    True si el usuario supervisa al menos un equipo con al menos un miembro.
    """
    return Team.objects.filter(
        supervisor=user,
        members__isnull=False
    ).exists()
