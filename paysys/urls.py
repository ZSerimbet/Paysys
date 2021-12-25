"""paysys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path

from accounts.views import (
    accounts_list_view, account_detail_view,
    account_create_view, accounts_erase_view,
    account_refill_view, account_transfer_view,
)

urlpatterns = [
    path('', accounts_list_view, name='accounts_list_view'),
    path('accounts/<slug:uuid>/detail/', account_detail_view, name='account_detail_view'),
    path('accounts/<slug:uuid>/refill/', account_refill_view, name='account_refill_view'),
    path('accounts/<slug:uuid>/transfer/', account_transfer_view, name='account_transfer_view'),
    path('accounts/create/', account_create_view, name='account_create_view'),
    path('accounts/erase/', accounts_erase_view, name='accounts_erase_view'),
]
