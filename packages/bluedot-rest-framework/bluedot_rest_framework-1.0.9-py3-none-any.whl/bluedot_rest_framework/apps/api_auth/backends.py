import inspect
import warnings

from .import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.db.models import Exists, OuterRef, Q
from .models import AuthUser


class ModelBackend(BaseBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(AuthUser.USERNAME_FIELD)
        if username is None or password is None:
            return
        try:
            user = AuthUser.get_by_natural_key(
                username=username).first()
        except AuthUser.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            AuthUser().set_password(password)
        else:
            if user:
                if user.check_password(password) and self.user_can_authenticate(user):
                    return user

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None
