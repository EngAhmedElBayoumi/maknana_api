from django.contrib import admin
from .models import *

# import formate_html
from django.utils.html import format_html


admin.site.register(machine)
admin.site.register(factory)
admin.site.register(malfunction_request)
admin.site.register(malfunction_report)
admin.site.register(malfunction_invoice)
admin.site.register(automation_request)
admin.site.register(market_category)
admin.site.register(Contarct)

admin.site.register(market_order_request)




# Register your models here.

@admin.register(market_product)
class MarketProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'description', 'view_image', 'type')


    list_filter = ('category', 'type')
    search_fields = ('name', 'description')

    def view_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />'.format(obj.image.url))
        else:
            return 'No image'
    view_image.short_description = 'Image'