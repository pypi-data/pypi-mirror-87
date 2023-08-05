from datetime import datetime
from mongoengine import (
    Document, EmbeddedDocument, fields, PULL
)


class Wechat(Document):

    meta = {'collection': 'wechat'}
