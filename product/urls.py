"""jahad_amooz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path

from product import views, ajax

app_name = 'product'
urlpatterns = [
    path('', views.product, name='product'),
    path('add_product', views.add_product, name='add_product'),
    path('product_comparison', views.product_comparison, name='product_comparison'),
    path('ajax/add_field', ajax.add_field, name='add_field'),
    path('ajax/load_cat', ajax.load_cat, name='load_cat'),
    path('ajax/load_product', ajax.load_product, name='load_product'),
    path('ajax/add_compare', ajax.add_compare, name='add_compare'),
    path('ajax/search_field', ajax.search_field, name='search_field'),
    path('ajax/search_filtering', ajax.search_filtering, name='search_filtering'),
    path('product_list', views.product_list, name='product_list'),
    path('product_detail/<pk>', views.product_detail, name='product_detail'),
    path('ajax/favorite', ajax.favorite, name='favorite'),
    path('ajax/load_brand', ajax.load_brand, name='load_brand'),
]
