from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from .views import (
    homeView,
    itemDetail,
    cartList,
    add_cart,
    add_single,
    remove_cart,
    remove_single,
    remove_coupon,
    add_coupon,
    invoice,
    check,
    dboard,
    ViewData,
    send_order)


app_name = 'core'

urlpatterns = [
    path('', homeView.as_view(), name = 'home'),
    path('products/<slug>/', itemDetail.as_view(), name = 'product'),
    path('checkout/', check.as_view(), name = 'check'),
    path('add-to-cart/<slug>/', add_cart, name = 'Add'),
    path('cart-list/', cartList.as_view(), name = 'cartlist'),
    path('remove_single/<slug>', remove_single, name = 'remove1'),
    path('remove/<slug>', remove_cart, name = 'remove'),
    path('remove-coupon/', remove_coupon, name = 'remove_c'),
    path('add_single/<slug>', add_single, name = 'add1'),
    path('add_coupon/', add_coupon.as_view(), name='add_c'),
    path('invoice/', invoice.as_view(), name='invoice'),
    path('send-order/', send_order, name='send'),
    path('admin/', dboard.as_view(), name='dboard'),
    path('data/', ViewData.as_view(), name='da'),
]