"""buildino URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from django.views.static import serve

from buildino import settings
from page import views

from provider import views as provider_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index_view, name="index"),
    path('blog/', include('blog.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('accounts/', include('accounts.urls')),
    path('provider/', include('provider.urls')),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^product/', include('product.urls')),
    path('product_detail', TemplateView.as_view(template_name='product_detail.html'), name="product_detail"),
    path('product_search', TemplateView.as_view(template_name='search.html'), name="product_search"),
    path('product_comparison', TemplateView.as_view(template_name='comparison.html'), name="product_comparison"),
    path('product_cart', TemplateView.as_view(template_name='cart.html'), name="product_cart"),
    path('register_login', TemplateView.as_view(template_name='register_login.html'), name="register_login"),
    path('edit_profile', TemplateView.as_view(template_name='profile/edit_profile.html'), name="edit_profile"),
    path('order_history', TemplateView.as_view(template_name='profile/order_history.html'), name="order_history"),
    path('add_shop', TemplateView.as_view(template_name='profile/add_shop.html'), name="add_shop"),
    path('add_product', TemplateView.as_view(template_name='profile/add_product.html'), name="add_product"),
    path('change_password', TemplateView.as_view(template_name='profile/change_password.html'), name="change_password"),
    path('forget_password', TemplateView.as_view(template_name='forget_password.html'), name="forget_password"),
    path('logout', TemplateView.as_view(template_name='profile/logout.html'), name="logout"),
    path('brands', provider_views.brand_list, name="brands"),
    path('brand_detail/<pk>', provider_views.brand_detail, name="brand_detail"),

    # New Dashboard Urls
    path('metronic', TemplateView.as_view(template_name='metronic/base-metronic.html'), name="metronic"),
    path('metronic/edit_profile', TemplateView.as_view(template_name='metronic/edit_profile.html'), name="edit_profile"),
    path('metronic/brand_status', TemplateView.as_view(template_name='metronic/brand_status.html'), name="brand_status"),
    path('metronic/shop_status', TemplateView.as_view(template_name='metronic/shop_status.html'), name="shop_status"),
    path('metronic/favorite_list', TemplateView.as_view(template_name='metronic/favorite_list.html'), name="favorite_list"),
    path('metronic/product_list', TemplateView.as_view(template_name='metronic/product_list.html'), name="product_list"),
    path('metronic/submit_shop', TemplateView.as_view(template_name='metronic/submit_shop.html'), name="submit_shop"),
    path('metronic/submit_product', TemplateView.as_view(template_name='metronic/submit_product.html'), name="submit_product"),
    path('metronic/add_shop_wizard', TemplateView.as_view(template_name='metronic/add_shop_wizard.html'), name="add_shop_wizard"),
    path('metronic/statistics', TemplateView.as_view(template_name='metronic/statistics.html'), name="statistics"),
    path('metronic/datatable', TemplateView.as_view(template_name='metronic/Transactions.html'), name="datatable"),




]


if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', serve),
    ]
