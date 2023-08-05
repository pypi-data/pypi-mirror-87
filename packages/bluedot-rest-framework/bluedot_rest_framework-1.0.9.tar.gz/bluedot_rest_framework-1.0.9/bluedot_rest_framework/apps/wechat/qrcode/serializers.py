from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import WeChatQrcode


class WeChatQrcodeSerializer(DocumentSerializer):

    class Meta:
        model = WeChatQrcode
        fields = '__all__'
