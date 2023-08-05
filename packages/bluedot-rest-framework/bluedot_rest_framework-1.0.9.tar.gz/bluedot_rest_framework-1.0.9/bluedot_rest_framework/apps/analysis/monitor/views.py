from rest_framework.response import Response
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet
from .models import Monitor
from .serializers import MonitorSerializer


class MonitorView(CustomModelViewSet):
    model_class = Monitor
    serializer_class = MonitorSerializer
    permission_classes = []
