
import base64
import json

from redis import Redis
from Crypto.Cipher import AES
from wechatpy.client import WeChatClient
from wechatpy.oauth import WeChatOAuth
from wechatpy.session.redisstorage import RedisStorage
from django.conf import settings


redis_client = Redis.from_url(settings.WECHAT['redis_client'])
session_interface = RedisStorage(
    redis_client,
    prefix='wechatpy'
)
MiniProgram = WeChatClient(
    settings.WECHAT['MINIPROGRAM']['APPID'],
    settings.WECHAT['MINIPROGRAM']['SECRET'],
    session=session_interface
)

OfficialAccount = WeChatClient(
    settings.WECHAT['OFFIACCOUNT']['APPID'],
    settings.WECHAT['OFFIACCOUNT']['SECRET'],
    session=session_interface
)


def official_account_oauth(redirect_uri, scope='snsapi_base', state=''):
    return WeChatOAuth(
        settings.WECHAT['OFFIACCOUNT']['APPID'],
        settings.WECHAT['OFFIACCOUNT']['SECRET'],
        redirect_uri,
        scope,
        state
    )


class WXBizDataCrypt:
    def __init__(self, appId, sessionKey):
        self.appId = appId
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)

        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)

        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
