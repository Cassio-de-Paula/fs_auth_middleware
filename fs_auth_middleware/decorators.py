from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from .utils import *

def has_permissions(required_permissions):
    """
    Decorator para function-based views que exige todas as permissões do token JWT vindo do cookie access_token.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            access_token = get_access_token_from_request(request)

            if not access_token:
                # Extrai a chave do sistema dos cookies
                system_id = get_system_key_from_request(request)

                if not system_id:
                    return Response({'message': 'Acesso não autorizado.'}, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    if request.method != 'GET':
                        return Response({'message': 'Método inválido para esta credencial'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
                    
                    # Tenta buscar um sistema que corresponda a chave recebida
                    is_valid, error_message = validate_system(system_id)

                    if not is_valid:
                        if error_message:
                            return Response({'message': error_message}, status=status.HTTP_401_UNAUTHORIZED)
                        return Response({'message': 'Credencial de sistema inválida'}, status=status.HTTP_401_UNAUTHORIZED)
                    
                    return view_func(request, *args, **kwargs)
            else:
                jwt_payload = decode_access_token(access_token, request)
                if not jwt_payload:
                    return Response({'message': 'Token inválido ou expirado.'}, status=status.HTTP_401_UNAUTHORIZED)

                is_active = validate_user_is_active(jwt_payload['user_id'])
                if not is_active:
                    response = Response({'message': 'Usuário inativo.'}, status=status.HTTP_401_UNAUTHORIZED)
                    response.delete_cookie('access_token')
                    response.delete_cookie('refresh_token', path='/session/')
                    return response

                user_permissions = jwt_payload.get('permissions', [])
            
            if all(p in user_permissions for p in required_permissions):
                return view_func(request, *args, **kwargs)

            return Response({'message': 'Permissão negada.'}, status=status.HTTP_403_FORBIDDEN)
        return _wrapped_view
    return decorator
