import time
import random
import string
from urllib import parse
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from wechatpy import parse_message, create_reply, utils
from bluedot_rest_framework.utils.jwt_token import jwt_create_token_wechat
from apps.user.models import User as UesrModel
from apps.user.serializers import UserSerializer
from . import MiniProgram, OfficialAccount, WXBizDataCrypt, official_account_oauth


class JSSdk(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        referer = request.META['HTTP_REFERER']

        ticket = OfficialAccount.jsapi.get_jsapi_ticket()
        nonceStr = ''.join(random.sample(
            string.ascii_letters + string.digits, 8))
        timestamp = str(int(time.time()))
        signature = OfficialAccount.jsapi.get_jsapi_signature(
            nonceStr, ticket, timestamp, referer)
        return Response({
            'appId': settings.WECHAT['OFFIACCOUNT']['APPID'],
            'timestamp': timestamp,
            'nonceStr': nonceStr,
            'signature': signature,
        })


class Auth(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, *args, **kwargs):
        code = request.GET.get('code')
        session_info = MiniProgram.wxa.code_to_session(code)
        user_openid = {'openid': session_info['openid']}
        user_obj = UesrModel.objects.filter(**user_openid).first()
        if user_obj is None:
            user_obj = UesrModel.objects.create(**user_openid)
        response = UserSerializer(user_obj).data
        unionid = ''
        if 'unionid' in response:
            unionid = response['unionid']
        response['session_key'] = session_info['session_key']
        response['token'] = jwt_create_token_wechat(
            session_info['openid'], unionid, response['id'])
        return Response(response)

    def post(self, request, *args, **kwargs):
        auth_data = request.data['data']
        auth_user = WXBizDataCrypt(
            settings.WECHAT['MINIPROGRAM']['APPID'], auth_data['session_key']
        ).decrypt(auth_data['encryptedData'], auth_data['iv'])
        user_data = {
            'unionid': auth_user['unionId'],
            'wechat_profile': {
                'nick_name': auth_user['nickName'],
                'avatar_url': auth_user['avatarUrl'],
                'gender': auth_user['gender'],
                'language': auth_user['language'],
                'city': auth_user['city'],
                'province': auth_user['province'],
                'country': auth_user['country'],
            }
        }

        UesrModel.objects.filter(
            openid=auth_user['openId']).update(**user_data)
        user = UesrModel.objects.get(openid=auth_user['openId'])
        user = UserSerializer(user).data
        user['token'] = jwt_create_token_wechat(
            user['openid'], user['unionid'], user['id'])
        return Response(user)


class OAuth(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        redirect_uri = "http://" + request.get_host() + request.get_full_path()
        code = request.query_params.get('code', None)
        referer_uri = request.query_params.get('referer_uri', None)

        if code:
            wechat_oauth = official_account_oauth(
                redirect_uri, 'snsapi_userinfo')
            wechat_oauth.fetch_access_token(code)
            user_info = wechat_oauth.get_user_info()

            user_data = {
                'unionid': user_info.get('unionid', ''),
                'openid': user_info.get('openid', ''),
                'wechat_profile': {
                    'nick_name': user_info.get('nickname', ''),
                    'avatar_url': user_info.get('headimgurl', ''),
                    'gender': user_info.get('sex', ''),
                    'province': user_info.get('province', ''),
                    'city': user_info.get('city', ''),
                    'country': user_info.get('country', ''),
                    'language': user_info.get('language', '')
                }
            }

            user_queryset = UesrModel.objects.filter(
                openid=user_info['openid']).first()
            if user_queryset:
                user_queryset.update(**user_data)
            else:
                user_queryset = UesrModel.objects.create(**user_data)

            token = jwt_create_token_wechat(
                openid=user_queryset.openid, unionid=user_queryset.unionid, userid=str(user_queryset.pk))

            link_type = '?'
            if "?" in referer_uri:
                link_type = '&'

            return HttpResponseRedirect(referer_uri + link_type + 'token=' + token)

        else:
            referer_uri = parse.quote(request.META['HTTP_REFERER'])
            link_type = '?'
            if "?" in referer_uri:
                link_type = '&'
            wechat_oauth = official_account_oauth(
                redirect_uri + link_type + 'referer_uri=' + referer_uri, 'snsapi_userinfo')
            url = wechat_oauth.authorize_url
            return HttpResponseRedirect(url)


class Token(APIView):
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        data = request.data
        user_queryset = UesrModel.objects.filter(openid=data['openid']).first()
        if user_queryset is None:
            user_queryset = UesrModel.objects.create(**data)
        token = jwt_create_token_wechat(
            openid=user_queryset.openid, unionid=user_queryset.unionid, userid=str(user_queryset.pk))
        return Response({'token': token})


class Menu(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        token = request.query_params.get('token', None)
        if token == 'e3340768d695c1591f352456ad51ab1c':
            OfficialAccount.menu.create({
                "button": [
                    {
                        "name": "关于我们",
                        "sub_button": [
                            {
                                "type": "miniprogram",
                                "name": "最新资讯",
                                "url": "http://cpa-global-wechat.bluewebonline.com/html/white_paper?source=menu",
                                "appid": "wx4c41efd924f3ef12",
                                "pagepath": "pages/index/index"
                            },
                            {
                                "type": "view",
                                "name": "资料中心",
                                "url": "http://cpa-global-wechat.bluewebonline.com/html/white_paper?source=menu",
                            },
                            {
                                "type": "view",
                                "name": "产品及解决方案",
                                "url": "http://cpa-global-wechat.bluewebonline.com/html/product?source=menu"
                            },
                        ]
                    },
                    {
                        "type": "view",
                        "name": "活动中心",
                        "url": "http://cpa-global-wechat.bluewebonline.com/html/home?source=menu"
                    },
                    {
                        "type": "view",
                        "name": "联系我们",
                        "url": "http://cpa-global-wechat.bluewebonline.com/html/contact_us?source=menu"
                    },
                ],
            })
        return Response()
