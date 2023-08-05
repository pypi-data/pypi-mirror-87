from mongoengine import (
    Document, EmbeddedDocument, fields, PULL, QuerySetManager
)
from django.contrib.auth.hashers import make_password
from mongoengine.queryset.manager import queryset_manager

from .base_user import AbstractUser


class AuthPermissions(Document):
    url = fields.StringField(max_length=150)
    method = fields.StringField(max_length=32)
    is_verify = fields.BooleanField(default=True)

    meta = {'collection': 'auth_permission'}


class AuthMenu(Document):
    path = fields.StringField(max_length=150)
    name = fields.StringField(max_length=150)
    icon = fields.StringField(max_length=150)
    parent = fields.ReferenceField('self', reverse_delete_rule=PULL)
    is_menu = fields.IntField()
    sort = fields.SequenceField()
    # permission_id = fields.ReferenceField(AuthPermissions)
    meta = {'collection': 'auth_menu'}


class AuthGroup(Document):
    name = fields.StringField(max_length=150)
    menu_ids = fields.ListField(fields.ReferenceField(AuthMenu))
    # permission_ids = fields.ListField(fields.ReferenceField(AuthPermissions))
    meta = {'collection': 'auth_group'}


class AuthUser(AbstractUser):

    group_ids = fields.ListField(fields.ReferenceField(AuthGroup))

    meta = {'collection': 'auth_user'}
