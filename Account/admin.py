from django.contrib import admin

from .models import *

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("username", "pk", "first_name", "last_name", "name", "email", "slug", "groups", "address",)


class AddressAdmin(admin.ModelAdmin):    
    list_display = ("country", "state", "city", "district", )

    # def related_user_name(self, obj):
    #         return  CustomUser.objects.get(address=obj).name

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Address, AddressAdmin)