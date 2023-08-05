import jwt
from datetime import datetime
from django.conf import settings
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.utils import jwt_get_secret_key

from bluedot_rest_framework.apps.api_auth.serializers import AuthUserSerializer


def jwt_response_payload_handler_admin(token, user=None, request=None):
    return {
        'token': token,
        'user': AuthUserSerializer(user, context={'request': request}).data
    }


def jwt_payload_handler_wehat(openid, unionid, userid):
    payload = {
        'user_id': settings.JWT_AUTH['SUPERUSER_ID'],
        'username': settings.JWT_AUTH['SUPERUSER_NAME'],
        'openid': openid,
        'unionid': unionid,
        'userid': userid,
        'exp': datetime.now() + api_settings.JWT_EXPIRATION_DELTA
    }
    if api_settings.JWT_ALLOW_REFRESH:
        payload['orig_iat'] = datetime.now().utctimetuple()

    if api_settings.JWT_AUDIENCE is not None:
        payload['aud'] = api_settings.JWT_AUDIENCE

    if api_settings.JWT_ISSUER is not None:
        payload['iss'] = api_settings.JWT_ISSUER
    return payload


def jwt_create_token_wechat(openid, unionid, userid=''):
    """
    创建token
    """
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler_wehat(openid, unionid, userid)
    token = jwt_encode_handler(payload)
    return token


def jwt_decode_handler_wechat(token):

    options = {
        'verify_exp': api_settings.JWT_VERIFY_EXPIRATION,
    }
    # get user from token, BEFORE verification, to get user secret key
    unverified_payload = jwt.decode(token, None, False)
    secret_key = jwt_get_secret_key(unverified_payload)
    return jwt.decode(
        token,
        api_settings.JWT_PUBLIC_KEY or secret_key,
        api_settings.JWT_VERIFY,
        options=options,
        leeway=api_settings.JWT_LEEWAY,
        audience=api_settings.JWT_AUDIENCE,
        issuer=api_settings.JWT_ISSUER,
        algorithms=[api_settings.JWT_ALGORITHM]
    )


def jwt_get_openid_handler(token):
    return jwt_decode_handler_wechat(token)['openid']


def jwt_get_unionid_handler(token):
    return jwt_decode_handler_wechat(token)['unionid']


def jwt_get_userid_handler(token):
    return jwt_decode_handler_wechat(token)['userid']


def jwt_get_userinfo_handler(token):
    return jwt_get_userid_handler(token), jwt_get_openid_handler(token), jwt_get_unionid_handler(token)
