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
            kid = headers.get("kid")
            if not kid:
                return None

            secret_key = get_secret_key_from_base_system(kid)
            return jwt.decode(token, secret_key, algorithms=["HS256"])
        except Exception as e:
            return None
    except (jwt.ExpiredSignatureError, jwt.DecodeError):
        return None

def get_secret_key_from_base_system(kid: str, original_request) -> str:
    access_token = original_request.COOKIES.get("access_token")

    headers = {}
    cookies = {}

    if access_token:
        cookies["access_token"] = access_token  # passa o mesmo cookie

    response = requests.get(
        f"https://{settings.BASE_SYSTEM_URL}/system/{kid}/",
        params={"kid": kid},
        cookies=cookies,  # repassa cookies
        timeout=5  # sempre bom ter timeout
    )

    if response.status_code == 200:
        return response.json().get("secret_key")

    raise ValueError("Chave não encontrada no sistema base")