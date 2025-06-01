from functools import wraps
from rest_framework.response import Response
from rest_framework import status

def has_any_permission(required_permissions):
    """
    Decorator para function-based views que exige pelo menos uma permissão do token JWT.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            jwt_payload = getattr(request, 'auth', {})
            user_permissions = jwt_payload.get('permissions', [])

            if any(p in user_permissions for p in required_permissions):
                return view_func(request, *args, **kwargs)

            return Response({'message': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)

        return _wrapped_view
    return decorator
