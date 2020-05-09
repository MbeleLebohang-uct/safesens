import graphene

from safesens.account.schema import AccountQuery, AccountMutation
from safesens.device.schema import DeviceQuery, DeviceMutation
from safesens.event.schema import EventQuery


class Query(
    AccountQuery,
    DeviceQuery,
    EventQuery
):
    pass

class Mutation(
    AccountMutation,
    DeviceMutation
):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
