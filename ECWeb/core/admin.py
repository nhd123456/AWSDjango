from django.contrib import admin
from django.db.models import Count, Sum
from .models import Item, OrderList, OrderedItem, coupon, blog_images, intro_images
import math
from django.contrib.admin.sites import AdminSite

# Register your models here.
admin.site.register(intro_images)
admin.site.register(blog_images)
admin.site.site_header = 'Dashboard'

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'volume')

@admin.register(OrderList)
class OIAdmin(admin.ModelAdmin):
    list_display = ('user', 'ordered_date', 'has_coupon')

@admin.register(OrderedItem)
class OLAdmin(admin.ModelAdmin):
    list_display = ('item', 'quantity')

@admin.register(coupon)
class cpAdmin(admin.ModelAdmin):
    list_display = ('code', 'saved')
