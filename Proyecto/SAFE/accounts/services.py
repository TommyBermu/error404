from django.core.exceptions import PermissionDenied
from accounts.models import AppUser, RoleChangeLog

def change_role(actor: AppUser, target: AppUser, new_role: str) -> bool:
    """
    Caso de uso RF_3:
    El Analista TH actualiza el rol de un usuario.
    """
    # 1. Validar que actor sea analista TH
    if actor.role != AppUser.UserRole.ANALISTA_TH:
        raise PermissionDenied("No tienes permisos para cambiar roles.")

    # 2. Validar que el rol nuevo sea válido
    valid_roles = dict(AppUser.UserRole.choices).keys()
    if new_role not in valid_roles:
        raise ValueError("Rol inválido.")

    # Prevenir que un usuario cambie su propio rol
    if actor.id == target.id:
        raise PermissionDenied("No puedes cambiar tu propio rol.")

    # 3. Guardar cambio en BD
    old_role = target.role
    target.role = new_role
    target.save()

    # 4. Registrar auditoría
    RoleChangeLog.objects.create(
        changed_by=actor,
        target_user=target,
        old_role=old_role,
        new_role=new_role
    )
    return True
