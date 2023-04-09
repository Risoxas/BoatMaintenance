from django.contrib import admin

from .models import Boats

# Register your models here.


class BoatAdmin(admin.ModelAdmin):
    readonly_fields = ['img_preview']


admin.site.register(Boats, BoatAdmin)
