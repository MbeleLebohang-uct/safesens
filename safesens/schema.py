import graphene

from safesens.account.schema import AccountQuery, AccountMutation
from safesens.device.schema import DeviceQuery
from safesens.event.schema import EventQuery


class Query(
    AccountQuery,
    DeviceQuery,
    EventQuery
):
    pass

class Mutation(
    AccountMutation
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
