from django.contrib import admin
from django.urls import reverse
from django.forms import Media

from .models import Boat, Customer, Employee, Order, Product, Order_Detail

# Register your models here.


class BoatAdmin(admin.ModelAdmin):
    readonly_fields = ['img_preview']


class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ('img_preview', 'mooring_no',)
    fields = ('customer', 'employee', 'order_date', 'boat_info', 'mooring_no', 'service_date', 'notes',
              'previous_image1', 'previous_image2', 'previous_image3', 'after_image1', 'after_image2', 'after_image3', 'img_preview')


admin.site.register(Boat, BoatAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register([Customer, Employee, Product, Order_Detail])
