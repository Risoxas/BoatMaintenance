from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Boats

# Register your models here.

admin.site.register(Boats)
