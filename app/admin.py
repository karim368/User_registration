from django.contrib import admin

# Register your models here.

from app.models import *

class Custom1(admin.ModelAdmin):
    list_display = ['username','address']

admin.site.register(Profile,Custom1)