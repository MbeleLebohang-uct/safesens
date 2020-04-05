import graphene

from safesens.account.schema import AccountQuery
from safesens.device.schema import DeviceQuery
from safesens.event.schema import EventQuery


class Query(
    AccountQuery,
    DeviceQuery,
    EventQuery
):
    pass


schema = graphene.Schema(query=Query)