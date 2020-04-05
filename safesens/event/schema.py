import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from ..account.models import User
from .models import Event

class EventFilter(django_filters.FilterSet):
    class Meta:
        model = Event
        fields = ['imei']

class EventNode(DjangoObjectType):
    class Meta:
        model = Event
        fields = []
        interfaces = (graphene.relay.Node, )

class EventQuery(graphene.ObjectType):
    event = graphene.relay.Node.Field(EventNode)
    all_events = DjangoFilterConnectionField(EventNode, filterset_class=EventFilter)
