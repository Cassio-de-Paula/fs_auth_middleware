import jwt
from django.conf import settings

def get_access_token_from_request(request):
    return request.COOKIES.get('access_token')

def decode_access_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        return payload
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None
