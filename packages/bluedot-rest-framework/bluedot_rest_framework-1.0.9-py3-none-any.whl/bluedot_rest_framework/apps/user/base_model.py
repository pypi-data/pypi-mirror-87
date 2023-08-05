from datetime import datetime
from mongoengine import (
    Document, EmbeddedDocument, fields
)


class Profile(EmbeddedDocument):
    first_name = fields.StringField(max_length=100)
    last_name = fields.StringField(max_length=100)
    email = fields.StringField(max_length=100)
    tel = fields.StringField(max_length=100)
    company = fields.StringField(max_length=100)
    job = fields.StringField(max_length=100)
    country = fields.StringField(max_length=100)
    source_type = fields.StringField(max_length=100, null=True)

    meta = {'abstract': True}


class WechatProfile(EmbeddedDocument):
    nick_name = fields.StringField(max_length=100)
    avatar_url = fields.StringField(max_length=255)
    gender = fields.IntField(max_length=10)

    province = fields.StringField(max_length=100)
    city = fields.StringField(max_length=100)
    country = fields.StringField(max_length=100)

    language = fields.StringField(max_length=100)
    meta = {'abstract': True}


class AbstractUser(Document):
    unionid = fields.StringField(max_length=100)
    openid = fields.StringField(max_length=100)

    wechat_profile = fields.EmbeddedDocumentField(WechatProfile)

    profile = fields.EmbeddedDocumentField(Profile)

    created = fields.DateTimeField(default=datetime.now)
    updated = fields.DateTimeField(default=datetime.now)

    meta = {'allow_inheritance': True, 'abstract': True}
