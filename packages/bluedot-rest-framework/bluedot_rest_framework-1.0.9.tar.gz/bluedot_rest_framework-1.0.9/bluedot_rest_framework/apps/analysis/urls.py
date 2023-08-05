from rest_framework.routers import DefaultRouter
from .monitor.views import MonitorView

router = DefaultRouter(trailing_slash=False)

router.register(r'analysis/monitor', MonitorView, basename='analysis-monitor')

urlpatterns = router.urls
