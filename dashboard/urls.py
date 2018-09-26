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

from dashboard import views

app_name = 'dashboard'
urlpatterns = [
    path('', views.dashboard_index, name='dashboard_index'),
    path('create', views.create_post, name='blog_create_post'),
    path('post_list', views.all_blog_post_index, name='all_post_list'),
    path('<int:pk>/edit', views.post_edit, name='blog_post_edit'),
    path('<int:year>/<int:month>/<int:day>/<slug>/delete', views.post_delete, name='blog_post_delete')
    # re_path(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$', views)
]

