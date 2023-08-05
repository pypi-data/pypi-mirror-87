from datetime import datetime
from mongoengine import (
    Document, EmbeddedDocument, fields
)


class WeChatQrcode(Document):
    user_name = fields.StringField(max_length=32)
    param = fields.DynamicField()
    url = fields.StringField(max_length=255)

    created = fields.DateTimeField(default=datetime.now)

    meta = {'collection': 'wechat_qrcode'}
