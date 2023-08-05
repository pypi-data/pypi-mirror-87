from rest_framework_mongoengine.serializers import DocumentSerializer
from .models import Monitor


class MonitorSerializer(DocumentSerializer):

    def create(self, validated_data):
        request = self.context['request']
        ip = request.META.get('HTTP_X_FORWARDED_FOR') if request.META.get(
            'HTTP_X_FORWARDED_FOR') else request.META.get('REMOTE_ADDR')
        validated_data['user']['ip'] = ip
        return self.Meta.model.objects.create(**validated_data)

    class Meta:
        model = Monitor
        fields = '__all__'
