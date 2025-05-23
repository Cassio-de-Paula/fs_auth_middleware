from rest_framework.permissions import BasePermission

class HasAnyPermission(BasePermission):
    """
    Permite acesso se o token JWT contiver pelo menos uma das permissões requeridas.
    """

    def has_permission(self, request, view):
        user_permissions = request.auth.get('permissions', []) if request.auth else []
        required_permissions = getattr(view, 'required_permissions', [])
        return any(p in user_permissions for p in required_permissions)
