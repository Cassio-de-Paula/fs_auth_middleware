from rest_framework.permissions import BasePermission

class HasAnyPermission(BasePermission):
    """
    Permite acesso se o token JWT contiver pelo menos uma das permissões requeridas.
    """

    def has_permission(self, request, view):
        jwt_payload = getattr(request, 'auth', None)

        if not jwt_payload or not isinstance(jwt_payload, dict):
            return False  # Token ausente ou malformado

        user_permissions = jwt_payload.get('permissions', [])
        required_permissions = getattr(view, 'required_permissions', [])

        return any(p in user_permissions for p in required_permissions)

class HasEveryPermission(BasePermission):
    """
    Permite acesso se o token JWT contiver todas as permissões requeridas.
    """

    def has_permission(self, request, view):
        jwt_payload = getattr(request, 'auth', None)

        if not jwt_payload or not isinstance(jwt_payload, dict):
            return False  # Token ausente ou malformado

        user_permissions = jwt_payload.get('permissions', [])
        required_permissions = getattr(view, 'required_permissions', [])

        return all(p in user_permissions for p in required_permissions)
    
class IsAuthenticated(BasePermission):
    """
    Permite acesso se houver um token JWT.
    """

    def has_permission(self, request, view):
        jwt_payload = getattr(request, 'auth', None)

        if not jwt_payload or not isinstance(jwt_payload, dict):
            return False  # Token ausente ou malformado
        else:
            return True   