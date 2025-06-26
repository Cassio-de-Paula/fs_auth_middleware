from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .utils import get_access_token_from_request, decode_access_token

def has_any_permission(required_permissions):
    """
    Decorator para function-based views que exige pelo menos uma permissão do token JWT vindo do cookie access_token.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            token = get_access_token_from_request(request)
            if not token:
                return Response({'message': 'Token de autenticação não fornecido.'}, status=status.HTTP_401_UNAUTHORIZED)

            jwt_payload = decode_access_token(token)
            if not jwt_payload:
                return Response({'message': 'Token inválido ou expirado.'}, status=status.HTTP_401_UNAUTHORIZED)

            user_permissions = jwt_payload.get('permissions', [])
            if any(p in user_permissions for p in required_permissions):
                return view_func(request, *args, **kwargs)

            return Response({'message': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)

        return _wrapped_view
    return decorator

def has_every_permission(required_permissions):
    """
    Decorator para function-based views que exige todas as permissões do token JWT vindo do cookie access_token.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            token = get_access_token_from_request(request)
            if not token:
                return Response({'message': 'Token de autenticação não fornecido.'}, status=status.HTTP_401_UNAUTHORIZED)

            jwt_payload = decode_access_token(token)
            if not jwt_payload:
                return Response({'message': 'Token inválido ou expirado.'}, status=status.HTTP_401_UNAUTHORIZED)

            user_permissions = jwt_payload.get('permissions', [])
            if all(p in user_permissions for p in required_permissions):
                return view_func(request, *args, **kwargs)

            return Response({'message': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)

        return _wrapped_view
    return decorator

def is_authenticated():
    """Decorator para verificar se o usuário está autenticado"""
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            token = get_access_token_from_request(request)

            if not token:
                return Response({'message': 'Necessário autenticar-se'}, status=status.HTTP_401_UNAUTHORIZED)
            
            jwt_payload = decode_access_token(token)
            if not jwt_payload:
                return Response({'message': 'Token inválido ou expirado.'}, status=status.HTTP_401_UNAUTHORIZED)

            return view_func(request, *args, **kwargs)

        return _wrapped_view
    return decorator