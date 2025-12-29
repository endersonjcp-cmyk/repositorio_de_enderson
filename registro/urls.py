"""
URL configuration for registro project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from motos import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('motos/', views.view_motorcycles, name='motos'),
    path('motos/registro/', views.register_motorcycle, name='register_moto'),
    path('singup/', views.singup, name='singup'),
    path('singin/', views.singin, name='singin'),
    path('logout/', views.singout, name='logout'),
    path('motos/editar/<int:moto_id>/', views.edit_motorcycle, name='edit_motorcycle'),
path('estadisticas/', views.estadisticas, name='estadisticas'),

]
