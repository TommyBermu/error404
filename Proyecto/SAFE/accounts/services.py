from django.db import transaction

from .models import AppUser


def change_role(actor: AppUser, target: AppUser, new_role: str) -> bool:
    """Change the role of ``target`` when performed by an authorized actor.

    Only ``AppUser.UserRole.ANALISTA_TH`` users can change roles. The new role
    must be a valid choice declared in ``AppUser.UserRole``. The operation is
    blocked when the actor attempts to change their own role. Returns ``True``
    when the role was updated and ``False`` otherwise.
    """

    if actor.role != AppUser.UserRole.ANALISTA_TH:
        return False

    valid_roles = {choice[0] for choice in AppUser.UserRole.choices}
    if new_role not in valid_roles:
        return False

    if actor.pk == target.pk:
        return False

    with transaction.atomic():
        target.role = new_role
        target.save(update_fields=["role", "updated_at"])

    return True
