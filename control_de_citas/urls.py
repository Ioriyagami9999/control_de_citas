"""
URL configuration for control_de_citas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from citas.views import index,login_s, password_reset_request, register, custom_logout
from django.urls import path, include

urlpatterns = [
   # path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('login/', login_s, name='login'),
    path('logout/', custom_logout, name='logout'),
    path('anexo/', include('citas.urls')),
    path('password_reset/', password_reset_request, name='password_reset_request'),
    path('register/', register, name='register'),
    

]
