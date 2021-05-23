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
from django.urls import path,include
from . import views
import tables.views as v
urlpatterns = [
    path('',views.customerhome,name='customerhome'),
    path('purchase/<int:item_id>',views.Purchase,name='purchase'),
    path('subscribe/<int:ditem_id>', views.subscribe, name='subscribe'),
    path('cart/',views.cart,name='cart'),
    path('logout/',v.EndSession,name='EndSession'),
    path('BidRegister/<int:item_id>', views.RegisterBid, name='RegisterBid'),
    path('AuctionList/', views.AuctionList, name='AuctionList'),
    path('Auction/<int:auction_id>', views.Auction, name='Auction'),


]
