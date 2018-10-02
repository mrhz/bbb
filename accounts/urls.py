from django.urls import path

from accounts import views as account_view, ajax
from provider import views as provider_view
from product import views as product_view

app_name = 'accounts'
urlpatterns = [

    path('upgrade', provider_view.upgrade_account, name='upgrade'),
    path('profile', account_view.profile_view, name='profile'),
    path('edit_profile', account_view.edit_profile, name='edit_profile'),
    path('agency/submit_brand', provider_view.submit_brand, name='submit_brand'),
    path('agency/edit_brand/<id>', provider_view.edit_brand, name='edit_brand'),
    path('agency/edit_product/<id>', product_view.edit_product ,name='edit_product'),
    path('shop_status', account_view.account_shop_status, name='shop_status'),
    path('brand_status', account_view.account_brand_status, name='brand_status'),
    path('favorite_list', account_view.favorite_list, name='favorite_list'),
    path('del_favorite', ajax.del_favorite, name='del_favorite'),
    path('del_p', ajax.del_p, name='del_p'),
    path('p_list', account_view.p_list, name='p_list'),
]