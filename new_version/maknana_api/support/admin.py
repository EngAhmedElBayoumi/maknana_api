from django.contrib import admin
from .models import supportTicket
# Register your models here.

@admin.register(supportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'subject', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'subject')

