from django.conf import settings
from django.contrib.auth import load_backend


def get_user_model():
    """
    Return the User model that is active in this project.
    """
    return settings.AUTH_USER_MODEL_MONGODB


def get_username_field():
    try:
        username_field = get_user_model().USERNAME_FIELD
    except:
        username_field = 'username'

    return username_field
