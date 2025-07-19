from django.contrib import admin
from .models import Campaign
# Register your models here.

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'start_date', 'end_date', 'status', 'on_click', 'external_link', 'machine', 'factory', 'service', 'market', 'other')
