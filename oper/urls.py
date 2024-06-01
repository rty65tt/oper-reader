# -*- coding: utf-8 -*-

"""oper URL Configuration
URL configuration for oper project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

#from django.conf.urls import include, url
#from django.contrib import admin
from django.urls import path

from oper import views

#from django.shortcuts import redirect

from django.conf import settings
from django.conf.urls.static import static

from django.views.generic.base import RedirectView
favicon_ico_view = RedirectView.as_view(url='/stat/favicon.ico', permanent=True)
favicon_png_view = RedirectView.as_view(url='/stat/favicon.png', permanent=True)

urlpatterns = [

    path('news/read.php', views.forum),
    
    path('gallery/view.php', views.gallery),
    path('gallery/list.php', views.gallery),
    path('gallery/', views.gallery),

    path('news/archive.php', views.archive),

    path('video/view.php', views.stenogramma),
    path('video/list.php', views.stenogramma),

    path('donate/', views.donate),
    path('about', views.about),
    path('visitors/info.php', views.vinfo),
    #path('mail', views.mail),

    path('favicon.ico', favicon_ico_view),
    path('favicon.png', favicon_png_view),

    path('robots.txt', views.robots_txt_view),

    path('', views.main)
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

