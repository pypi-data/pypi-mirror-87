from rest_framework.decorators import action
from bluedot_rest_framework.utils.viewsets import CustomModelViewSet, TreeAPIView
from rest_framework.response import Response

from .models import Category
from .serializers import CategorySerializer


class CategoryView(CustomModelViewSet, TreeAPIView):
    model_class = Category
    serializer_class = CategorySerializer
    pagination_class = None

    filterset_fields = {
        '_type': {
            'type': 'int',
            'filter': ''
        },
        'title': {
            'type': 'string',
            'filter': '__contains'
        },
        'parent': {
            'type': 'string',
            'filter': ''
        },
    }

    @action(detail=False, methods=['post'], url_path='sort', url_name='sort')
    def sort(self, request, *args, **kwargs):
        before_sort = request.data.get('before_sort')
        before_id = request.data.get('before_id')
        after_sort = request.data.get('after_sort')
        after_id = request.data.get('after_id')
        self.model_class.objects.get(pk=before_id).update(sort=after_sort)
        self.model_class.objects.get(pk=after_id).update(sort=before_sort)
        return Response(status=200)
