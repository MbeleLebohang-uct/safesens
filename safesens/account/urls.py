from django.urls import path
from .views import account_confirm_view

urlpatterns = [
    path('account-confirm/', account_confirm_view, name='account-confirm'),
]