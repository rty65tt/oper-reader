# -*- coding: utf-8 -*-

"""oper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
#from django.contrib import admin
from oper import views

from django.shortcuts import redirect

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import RedirectView
favicon_ico_view = RedirectView.as_view(url='/stat/favicon.ico', permanent=True)
favicon_png_view = RedirectView.as_view(url='/stat/favicon.png', permanent=True)


urlpatterns = [
#    url(r'^admin/', include(admin.site.urls)),

    url(r'^news/read.php$', views.forum),
    
    url(r'^gallery/view.php$', views.gallery),
    url(r'^gallery/list.php$', views.gallery),
    url(r'^gallery/$', views.gallery),

    url(r'^news/archive.php', views.archive),

    url(r'^video/view.php', views.stenogramma),
    url(r'^video/list.php', views.stenogramma),

    url(r'^donate/([\w]+)', views.donate),
    url(r'^about', views.about),
    #url(r'^mail', views.mail),

    url(r'^favicon\.ico$', favicon_ico_view),
    url(r'^favicon\.png$', favicon_png_view),


    url(r'^$', views.main)
]  #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

