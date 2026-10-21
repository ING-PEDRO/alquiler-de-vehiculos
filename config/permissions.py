from rest_framework.permissions import SAFE_METHODS, BasePermission

ADMINISTRADOR = "Administrador"
ASESOR = "Asesor comercial"
JEFE_FLOTA = "Jefe de flota"
CLIENTE = "Cliente"
ROLES = [ADMINISTRADOR, ASESOR, JEFE_FLOTA, CLIENTE]


def grupos(user):
    return set(user.groups.values_list("name", flat=True))


class RolePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        g = grupos(user)
        if ADMINISTRADOR in g:
            return True
        por_accion = getattr(view, "roles_by_action", {})
        action = getattr(view, "action", None)
        if action in por_accion:
            permitidos = por_accion[action]
        elif request.method in SAFE_METHODS:
            permitidos = getattr(view, "roles_read", ())
        else:
            permitidos = getattr(view, "roles_write", ())
        return bool(g & set(permitidos))