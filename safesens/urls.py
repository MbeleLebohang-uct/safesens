"""
    safesens URL Configuration
"""
from django.contrib import admin
from django.urls import path
from safesens.pages.views import home_view
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from .schema import schema

urlpatterns = [
    path('', home_view, name='home'),
    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True,schema=schema))),
    path('admin/', admin.site.urls),
]
