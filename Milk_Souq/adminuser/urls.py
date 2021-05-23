"""Milk_Souq URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from . import views
import tables.views as v
urlpatterns = [
    path('',views.adminuser,name='adminuser'),
    path('itemadd/',views.itemadd,name='itemadd'),
    path('brandadd/',views.brandadd,name='brandadd'),
    path('deliveryadd/',views.deliveryadd,name='deliveryadd'),
    path('dailyitemadd/',views.dailyitemadd,name='dailyitemadd'),
    path('dailyitemcollection/',views.dailyitemcollection,name='dailyitemcollection'),
    path('discountadd/',views.DiscountAdd,name='DiscountAdd'),
    path('logout/', v.EndSession, name='EndSession'),


]