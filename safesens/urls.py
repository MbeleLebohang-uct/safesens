"""
    safesens URL Configuration
"""
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from django.conf.urls.static import static
from safesens.pages.views import home_view
from django.contrib.staticfiles.views import serve
from django.views.generic.base import RedirectView
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema

urlpatterns = [
    path('', home_view, name='home'),
    path('account/', include('safesens.account.urls')),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True,schema=schema))),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static("/media/", document_root=settings.MEDIA_ROOT) + [
        url(r"^static/(?P<path>.*)$", serve),
    ]
