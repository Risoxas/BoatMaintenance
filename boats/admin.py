from django.contrib import admin

from .models import Boat, Customer, Employee, Order, Shipping_Method, Product, Order_Detail, Payment_Method, Payment

# Register your models here.


class BoatAdmin(admin.ModelAdmin):
    readonly_fields = ['img_preview']


admin.site.register([Boat, Customer, Employee, Order,
                    Shipping_Method, Product, Order_Detail, Payment_Method, Payment])
