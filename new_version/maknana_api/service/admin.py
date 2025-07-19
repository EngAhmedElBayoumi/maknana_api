from django.contrib import admin
from .models import service, ServiceRequest , request_invoice, request_report
from django.utils.html import format_html
# Register your models here.

@admin.register(service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'view_image')

    def view_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 50px; height: 50px;"/>', obj.image.url)
        return "No Image"
    
    view_image.short_description = 'Image'

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('client', 'name')
    

@admin.register(request_invoice)
class ServiceRequestInvoiceAdmin(admin.ModelAdmin):
    list_display = ('service_request',)
    


@admin.register(request_report)
class ServiceRequestReportAdmin(admin.ModelAdmin):
    list_display = ('service_request',)
    

    