from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework_mongoengine.serializers import DocumentSerializer
from rest_framework_jwt.serializers import jwt_payload_handler, jwt_encode_handler
from rest_framework_jwt.compat import Serializer
from . import get_username_field

from .models import AuthUser, AuthMenu, AuthGroup, AuthPermissions


class AuthUserSerializer(DocumentSerializer):

    class Meta:
        model = AuthUser
        fields = '__all__'

    def create(self, validated_data):
        return AuthUser.create_user(**validated_data)

    def update(self, instance, validated_data):
        if validated_data.get('password', None):
            instance.set_password(validated_data.get(
                'password'))

        instance.group_ids = validated_data.get(
            'group_ids', instance.group_ids)
        instance.email = validated_data.get(
            'email', instance.email)
        instance.is_active = validated_data.get(
            'is_active', instance.is_active)
        instance.save()
        return instance


class AuthPermissionsSerializer(DocumentSerializer):

    class Meta:
        model = AuthPermissions
        fields = '__all__'


class AuthMenuSerializer(DocumentSerializer):

    class Meta:
        model = AuthMenu
        fields = '__all__'


class AuthGroupSerializer(DocumentSerializer):

    # menu = AuthMenuSerializer(source='menu_ids', read_only=True, many=True)

    class Meta:
        model = AuthGroup
        fields = '__all__'


class JSONWebTokenSerializer(Serializer):
    """
    Serializer class used to validate a username and password.

    'username' is identified by the custom UserModel.USERNAME_FIELD.

    Returns a JSON Web Token that can be used to authenticate later calls.
    """

    def __init__(self, *args, **kwargs):
        """
        Dynamically add the USERNAME_FIELD to self.fields.
        """
        super(JSONWebTokenSerializer, self).__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField()
        self.fields['password'] = serializers.CharField(write_only=True)

    @property
    def username_field(self):
        return get_username_field()

    def validate(self, attrs):
        credentials = {
            self.username_field: attrs.get(self.username_field),
            'password': attrs.get('password')
        }

        if all(credentials.values()):
            user = authenticate(**credentials)

            if user:
                if not user.is_active:
                    msg = _('User account is disabled.')
                    raise serializers.ValidationError(msg)
                user.pk = str(user.pk)
                payload = jwt_payload_handler(user)

                return {
                    'token': jwt_encode_handler(payload),
                    'user': user
                }
            else:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('Must include "{username_field}" and "password".')
            msg = msg.format(username_field=self.username_field)
            raise serializers.ValidationError(msg)
