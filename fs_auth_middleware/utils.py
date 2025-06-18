import jwt
from django.conf import settings
import requests

def get_access_token_from_request(request):
    return request.COOKIES.get('access_token')

def decode_access_token(token: str):
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    except jwt.InvalidSignatureError:
        try:
            headers = jwt.get_unverified_header(token)
            system_id = headers.get("kid")
            if not system_id:
                return None

            secret_key = get_secret_key_from_base_system(system_id)
            return jwt.decode(token, secret_key, algorithms=["HS256"])
        except Exception as e:
            return None
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        return None

def get_secret_key_from_base_system(system_id: str, original_request) -> str:
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
        return response.json().get("secret_key")

    raise ValueError("Chave não encontrada no sistema base")