import graphene
from graphene_django.types import DjangoObjectType
from django.db.models import Q
from .models import Event

class EventType(DjangoObjectType):
    class Meta:
        model = Event

class EventQuery(graphene.ObjectType):
    events = graphene.List(EventType, imei=graphene.String())

    def resolve_events(self, info, imei=None, **kwargs):
        if imei:
            return Event.objects.filter(Q(imei=imei))

        return None
