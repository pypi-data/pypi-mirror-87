from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from .qrcode.views import WeChatQrcodeView
from .template_message import event_register_template
from .views import JSSdk, Auth, OAuth, Token, Menu
from .response import Response


urlpatterns = [
    url(r'^wechat/auth', Auth.as_view()),
    url(r'^wechat/oauth', OAuth.as_view()),
    url(r'^wechat/token', Token.as_view()),
    url(r'^wechat/response', Response.as_view()),
    url(r'^wechat/jssdk', JSSdk.as_view()),
    url(r'^wechat/template_message/event_register_template',
        event_register_template),
    url(r'^wechat/menu', Menu.as_view()),
]

router = DefaultRouter(trailing_slash=False)

router.register(r'wechat/qrcode', WeChatQrcodeView,
                basename='wechat-qrcode')

urlpatterns += router.urls
