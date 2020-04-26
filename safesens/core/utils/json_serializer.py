from django.core.serializers.json import DjangoJSONEncoder

class CustomJsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        return super().default(obj)