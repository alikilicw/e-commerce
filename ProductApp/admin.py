from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from Account.models import *

class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "user", "selected_categories", "price", "currency")
    readonly_fields = ("slug",)

    def selected_categories(self, obj):
        html = "<ul>"

        for category in obj.category.all():
            html += "<li>" + category.name + "</li>"
        
        html += "</ul>"
        return mark_safe(html)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    readonly_fields = ("slug",)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ("from_user", "product", "to_user", "is_active", "review_date")  
    list_editable = ("is_active",)


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ("currency_type", "currency_symbol")  

admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Currency, CurrencyAdmin)

