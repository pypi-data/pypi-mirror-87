from django.conf import settings
from rest_framework import status
from rest_framework.views import APIView
from wechatpy import parse_message, create_reply, utils
from django.shortcuts import HttpResponse
from rest_framework.response import Response
from . import OfficialAccount


from bluedot_rest_framework.apps.analysis.monitor.models import Monitor


class Response(APIView):
    permission_classes = ()

    def get(self, request, *args, **kwargs):
        signature = request.GET.get('signature')
        timestamp = request.GET.get('timestamp')
        nonce = request.GET.get('nonce')
        echo_str = request.GET.get('echostr')
        token = settings.WECHAT['OFFIACCOUNT']['TOKEN']
        utils.check_signature(token, signature, timestamp, nonce)
        return HttpResponse(echo_str)

    def post(self, request, *args, **kwargs):
        msg = parse_message(request.body)
        msg_dict = msg.__dict__['_data']
        data = {
            'type': '微信响应日志',
            'user': {
                'openid': msg_dict['FromUserName'],
            },
            'wechat': {
                'user_name': msg_dict['ToUserName'],
                'appid': settings.WECHAT['OFFIACCOUNT']['APPID'],
                'name': '',
                'event': {
                    'key': '',
                    'msg': '',
                    'type': msg_dict['MsgType']
                }
            },
        }
        if 'EventKey' in msg_dict:
            data['wechat']['event']['key'] = msg_dict['Event']
        if 'Content' in msg_dict:
            data['wechat']['event']['msg'] = msg_dict['Content']
        elif msg_dict['MsgType'] == 'event':
            data['wechat']['event']['msg'] = msg_dict['EventKey']

        Monitor.objects.create(**data)

        default_subscribe_text = """感谢关注"""

        reply = create_reply(default_subscribe_text, msg)
        response = HttpResponse(
            reply.render(), content_type="application/xml")

        if msg.type == 'text':
            pass

        elif msg.type == 'event':

            if msg_dict['Event'] == 'unsubscribe':
                pass
            elif msg_dict['Event'] == 'SCAN' or msg_dict['Event'] == 'subscribe_scan':
                if 'filesdownload1030' in msg_dict['EventKey']:
                    text = """感谢关注"""
                    reply = create_reply(text, msg)

                    response = HttpResponse(
                        reply.render(), content_type="application/xml")
                else:
                    text = default_subscribe_text
                    reply = create_reply(text, msg)
                    response = HttpResponse(
                        reply.render(), content_type="application/xml")
            elif msg_dict['Event'] == 'subscribe':
                text = default_subscribe_text
                reply = create_reply(text, msg)
                response = HttpResponse(
                    reply.render(), content_type="application/xml")
        return response
