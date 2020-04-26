import graphene

from graphql_jwt.utils import jwt_payload


def create_jwt_payload(user, context=None):
    payload = jwt_payload(user, context)
    payload["user_id"] = graphene.Node.to_global_id("User", user.id)
    payload["is_staff"] = user.is_staff
    payload["role"] = user.role
    payload["is_superuser"] = user.is_superuser
    return payload