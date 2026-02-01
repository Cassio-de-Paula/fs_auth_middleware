from jwt import decode as jwt_decode, InvalidSignatureError, ExpiredSignatureError, DecodeError
from django.conf import settings
from django.contrib.auth import get_user_model
from django.apps import apps

def get_access_token_from_request(request):
    return request.COOKIES.get('access_token')

def get_system_key_from_request(request):
    return request.COOKIES.get('system')

def get_user_model_cls():
    return get_user_model()

def get_system_model_cls():
    model_path = getattr(settings, "FS_AUTH_SYSTEM_MODEL", None)
    if not model_path:
        return None
    return apps.get_model(model_path)

def is_valid_system_model(System) -> bool:
    if System is None:
        return False
    required_fields = {
        "id",
        "name",
        "system_url",
        "is_active",
        "api_key",
        "current_state",
        "secret_key",
        "dev_team",
    }
    model_fields = {f.name for f in System._meta.get_fields()}
    return required_fields.issubset(model_fields)

def decode_access_token(token: str, request):
    try:
        return jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except InvalidSignatureError:
        return None
    except (ExpiredSignatureError, DecodeError):
        return None
    
def validate_user_is_active(user_id: str):
    try:
        User = get_user_model_cls()
        user = User.objects.filter(pk=user_id).only("is_active").first()
        if not user:
            return False
        return bool(getattr(user, "is_active"))
    except Exception:
        return False
  
def validate_system(system_id: str) -> bool:
    try:
        System = get_system_model_cls()
        if System is None:
            return False, "Requisições entre sistemas não são autorizadas."
        if not is_valid_system_model(System):
            return False, "System model incompatível."
        exists = System.objects.filter(api_key=system_id).exists()
        return exists, None
    except Exception:
        return False, "Erro ao validar credencial de sistema."
