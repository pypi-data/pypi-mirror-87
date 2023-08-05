from rest_framework_mongoengine.serializers import DocumentSerializer


class CustomSerializer(DocumentSerializer):

    def __init__(self, *args, **kwargs):
        # Don't pass the 'fields' arg up to the superclass
        exclude_fields = kwargs.pop('exclude_fields', None)
        # include_fields = kwargs.pop('include_fields', None)

        # Instantiate the superclass normally
        super(CustomSerializer, self).__init__(*args, **kwargs)

        if exclude_fields:
            # Drop fields specified in the `fields` argument.
            banished = set(exclude_fields)
            for field_name in banished:
                self.fields.pop(field_name)
