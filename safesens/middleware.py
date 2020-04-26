from django.contrib.auth.models import AnonymousUser
from graphql_jwt.middleware import JSONWebTokenMiddleware

class JWTMiddleware(JSONWebTokenMiddleware):
    def resolve(self, next, root, info, **kwargs):
        request = info.context

        if not hasattr(request, "user"):
            request.user = AnonymousUser()
        return super().resolve(next, root, info, **kwargs)