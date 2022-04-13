"""search_cities URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
# server/search_cities/urls.py

from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from cities.views import upload
#from django.conf.urls.static import static

import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path("upload/",upload, name="upload"),
    path('api/v1/cities/', include('cities.urls')),
]

if settings.DEBUG or settings.TESTING_MODE: 
    urlpatterns = [
        path('debug/', include(debug_toolbar.urls)),
    ] + urlpatterns 
    #urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)