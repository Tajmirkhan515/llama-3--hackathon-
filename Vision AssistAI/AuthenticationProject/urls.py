"""
URL configuration for AuthenticationProject project.

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
from django.contrib import admin
from django.urls import path

from AuthenticationProject import settings
from MyApp import views
from MyApp.views import * # type: ignore
from django.conf import settings # type: ignore
from django.conf.urls.static import static # type: ignore

urlpatterns = [
   # path('', admin.site.urls),
    path('register/', register_view, name='register'), # type: ignore
    path('', login_view, name='login'), # type: ignore
    path('logout/', logout_view, name='logout'), # type: ignore
    path('dashboard/', dashboard_view, name='dashboard'), # type: ignore    
    path('upload-image/', handle_image_post, name='handle_image_post'),

    path('temp-file/<str:filename>/', views.serve_temp_file, name='serve_temp_file'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



