from datetime import datetime
from mongoengine import (
    Document, EmbeddedDocument, fields
)


class User(EmbeddedDocument):
    unionid = fields.StringField(max_length=100)
    openid = fields.StringField(max_length=100)
    ip = fields.StringField(max_length=100)
    network = fields.StringField(max_length=100)
    agent = fields.DynamicField(null=True)
    meta = {'abstract': True}


class PageEvent(EmbeddedDocument):
    key = fields.StringField(max_length=255)
    type = fields.StringField(max_length=100)
    meta = {'abstract': True}


class Page(EmbeddedDocument):
    title = fields.StringField(null=True)
    keywords = fields.ListField(fields.StringField(null=True))
    description = fields.StringField(null=True)

    url = fields.StringField(null=True)
    base_url = fields.StringField(null=True)
    param = fields.DynamicField(null=True)

    event = fields.EmbeddedDocumentField(PageEvent)

    meta = {'abstract': True}


class WeChatEvent(EmbeddedDocument):
    key = fields.StringField(null=True)
    msg = fields.DynamicField(null=True)
    type = fields.StringField(null=True)
    meta = {'abstract': True}


class WeChat(EmbeddedDocument):
    user_name = fields.StringField(null=True)
    appid = fields.StringField(null=True)
    name = fields.StringField(null=True)
    event = fields.EmbeddedDocumentField(WeChatEvent)
    label = fields.StringField(null=True)
    meta = {'abstract': True}


class Monitor(Document):
    type = fields.StringField(max_length=255)

    user = fields.EmbeddedDocumentField(User)
    page = fields.EmbeddedDocumentField(Page)
    wechat = fields.EmbeddedDocumentField(WeChat)

    created = fields.DateTimeField(default=datetime.now)
    updated = fields.DateTimeField(default=datetime.now)

    meta = {'collection': 'analysis_monitor'}
