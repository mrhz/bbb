from django.urls import path

from provider import ajax

app_name = 'provider'
urlpatterns = [

    path('submit_shop', ajax.submit_shop, name='submit_shop'),
]