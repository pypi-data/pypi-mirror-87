from datetime import datetime
from django.conf import settings
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from rest_framework_jwt.views import JSONWebTokenAPIView
from rest_framework_jwt.settings import api_settings

from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, TreeAPIView
from bluedot_rest_framework.utils.func import get_tree, get_tree_menu

from .serializers import JSONWebTokenSerializer, AuthUserSerializer, AuthMenuSerializer, AuthGroupSerializer, AuthPermissionsSerializer
from .models import AuthUser, AuthMenu, AuthGroup, AuthPermissions

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER


class LoginAPIView(JSONWebTokenAPIView):

    serializer_class = JSONWebTokenSerializer


class CurrentUserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        user = AuthUserSerializer(request.user, context={
            'request': request}).data
        return Response({**user, 'avatar': settings.JWT_AUTH['AVATAR']})


class AuthUserViewSet(CustomModelViewSet):
    model_class = AuthUser
    serializer_class = AuthUserSerializer

    permission_classes = [IsAdminUser]


class AuthGroupViewSet(CustomModelViewSet):
    model_class = AuthGroup
    serializer_class = AuthGroupSerializer

    permission_classes = [IsAdminUser]


class AuthPermissionsViewSet(CustomModelViewSet):
    model_class = AuthPermissions
    serializer_class = AuthPermissionsSerializer
    pagination_class = None

    permission_classes = [IsAdminUser]


class MenuViewSet(CustomModelViewSet, TreeAPIView):
    model_class = AuthMenu
    serializer_class = AuthMenuSerializer

    @action(detail=False, methods=['get'], url_path='current', url_name='current')
    def current(self, request, *args, **kwargs):
        if request.user.is_superuser:
            queryset = self.model_class.objects.filter(
                is_menu=1).order_by('-sort')
        else:
            user = AuthUserSerializer(request.user, context={
                                      'request': request}).data
            queryset = AuthGroup.objects.filter(
                pk__in=user['group_ids']).distinct('menu_ids')

        serializer = self.get_serializer(queryset, many=True)

        before_menu = serializer.data
        data = []
        for item in before_menu:
            data.append(item)
            if item['parent'] and get_tree_menu(data, item['parent']):
                queryset = self.model_class.objects.get(pk=item['parent'])
                data.append(self.get_serializer(queryset).data)
        data = get_tree(data, None)
        return Response(data)


login_url = LoginAPIView.as_view()
current_user_url = CurrentUserAPIView.as_view()
