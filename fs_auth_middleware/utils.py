from jwt import decode as jwt_decode, InvalidSignatureError, ExpiredSignatureError, DecodeError
from django.conf import settings
import requests

def get_access_token_from_request(request):
    return request.COOKIES.get('access_token')

def get_system_key_from_request(request):
    return request.COOKIES.get('system')

def decode_access_token(token: str, request):
    try:
        return jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    
    except InvalidSignatureError:
        system_id = request.COOKIES.get('system', None)

        if not system_id:
            return None

        try:
            return validate_system(system_id, request)
        except Exception:
            return None
    
    except (ExpiredSignatureError, DecodeError):
        return None
  
def validate_system(system_id: str) -> bool:
    response = requests.get(
        f"http://{settings.BASE_SYSTEM_URL}/system/get/{system_id}/",
        timeout=5
    )

    if response.status_code == 200:
        return True

    return False