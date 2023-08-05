from datetime import datetime
from mongoengine import (
    Document, EmbeddedDocument, fields, PULL
)


class Category(Document):
    _type = fields.IntField(max_length=10, default=1)
    title = fields.StringField(max_length=100, null=True)
    parent = fields.ReferenceField(
        'self', reverse_delete_rule=PULL)
    sort = fields.SequenceField()

    created = fields.DateTimeField(default=datetime.now)
    updated = fields.DateTimeField(default=datetime.now)

    meta = {'collection': 'category'}
