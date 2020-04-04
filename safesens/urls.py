"""
    safesens URL Configuration
"""
from django.contrib import admin
from django.urls import path
from safesens.pages.views import home_view
from graphene_django.views import GraphQLView
from .schema import schema

urlpatterns = [
    path('', home_view, name='home'),
    path("graphql/", GraphQLView.as_view(graphiql=True,schema=schema), name="graphql"),
    path('admin/', admin.site.urls),
]
