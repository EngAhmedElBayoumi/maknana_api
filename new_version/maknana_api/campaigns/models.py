from django.db import models
from machine_and_factory.models import machine, factory,market_product
from service.models import service

    
import uuid
import os

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join("uploads/images/", filename)


# Create your models here.
# name , start_date , end_date, status , الفئة المستهدفة , description
class Campaign(models.Model):
    name = models.CharField(max_length=255, verbose_name="Campaign Name")
    start_date = models.DateTimeField(verbose_name="Start Date")
    end_date = models.DateTimeField(verbose_name="End Date")
    status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('completed', 'Completed')
    ], default='active', verbose_name="Status")
    target_audience = models.TextField(verbose_name="Target Audience")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    attachment = models.FileField(upload_to=upload_to, blank=True, null=True, verbose_name="Attachment")
    on_click= models.CharField(
        max_length=50,
        choices=[
            ('market_page', 'Market Page'),
            ('service_page', 'Service Page'),
            ('factory_page', 'Factory Page'),
            ('machine_page', 'Machine Page'),
            ('other_page', 'Other Page'),
            ('external_link', 'External Link'),
        ],
        default='open_url',
        verbose_name="On Click Action"
    )
    external_link = models.URLField(blank=True, null=True, verbose_name="External Link")
    machine = models.ForeignKey(machine, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Machine")
    factory = models.ForeignKey(factory, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Factory")
    service = models.ForeignKey(service, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Service")
    market = models.ForeignKey(market_product, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Market")
    other = models.CharField(max_length=255, blank=True, null=True, verbose_name="Other Page")


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"

    class Meta:
        ordering = ['-id']