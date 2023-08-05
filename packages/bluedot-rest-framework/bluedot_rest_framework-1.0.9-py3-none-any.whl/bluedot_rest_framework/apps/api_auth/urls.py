from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import login_url, current_user_url, MenuViewSet, AuthUserViewSet, AuthGroupViewSet, AuthPermissionsViewSet

router = DefaultRouter(trailing_slash=False)

urlpatterns = [
    url(r'^auth/login', login_url),
    url(r'^auth/current-user', current_user_url)
]

router.register(r'auth/menu', MenuViewSet, basename='auth-menu')
router.register(r'auth/user', AuthUserViewSet, basename='auth-user')
router.register(r'auth/group', AuthGroupViewSet, basename='auth-group')
router.register(r'auth/permission',
                AuthPermissionsViewSet, basename='auth-permission')

urlpatterns += router.urls
