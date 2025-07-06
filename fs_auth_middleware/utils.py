from jwt import decode as jwt_decode, InvalidSignatureError, ExpiredSignatureError, DecodeError
from django.conf import settings
import requests

def get_access_token_from_request(request):
    return request.COOKIES.get('access_token')

def decode_access_token(token: str, request):
    from jwt import decode as jwt_decode, InvalidSignatureError, ExpiredSignatureError, DecodeError

    try:
        return jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    
    except InvalidSignatureError:
        system_id = request.COOKIES.get('system', None)
        if not system_id:
            return None

        try:
            validate_system(system_id, request)
            return True
        except Exception:
            return None
    
    except (ExpiredSignatureError, DecodeError):
        return None
  
def validate_system(system_id: str, original_request) -> str:
    access_token = original_request.COOKIES.get("access_token")

    cookies = {}

    if access_token:
        cookies["access_token"] = access_token

    response = requests.get(
        f"https://{settings.BASE_SYSTEM_URL}/system/get/{system_id}/",
        cookies=cookies,
        timeout=5
    )

    if response.status_code == 200:
        return response.json()

    raise ValueError("Chave não encontrada no sistema base")