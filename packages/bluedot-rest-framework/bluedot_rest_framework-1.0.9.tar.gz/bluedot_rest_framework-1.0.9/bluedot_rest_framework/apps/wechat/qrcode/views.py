from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
from . import CreateQrcode
from .models import WeChatQrcode
from .serializers import WeChatQrcodeSerializer


class WeChatQrcodeView(CustomModelViewSet):
    model_class = WeChatQrcode
    serializer_class = WeChatQrcodeSerializer

    @action(detail=False, methods=['post'], url_path='miniprogram', url_name='miniprogram')
    def miniprogram(self, request, *args, **kwargs):
        user_name = 'gh_5645640b48e2'
        page = request.data.get('page', None)
        param = request.data.get('param', None)

        data = WeChatQrcode.objects.filter(
            param=param).first()

        if data is None:
            qrcode = WeChatQrcode(
                user_name=user_name, param=param)
            qrcode.save()

            _id = str(qrcode.id)
            url = CreateQrcode.miniprogram(_id, page)

            qrcode.url = url
            qrcode.save()
        else:
            url = data.url

        return Response({'url': url})

    @action(detail=False, methods=['get'], url_path='offiaccount_event_live', url_name='offiaccount_event_live')
    def offiaccount_event_live(self, request, *args, **kwargs):
        event_id = request.query_params.get('event_id')
        scene_str = f"event_{event_id}"
        url = CreateQrcode.offiaccount_event_live(scene_str)

        return Response({'url': url})
