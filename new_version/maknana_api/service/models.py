from django.db import models
from core.models import CustomUser

import uuid
import os

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join("uploads/images/", filename)
# Create your models here.

class service(models.Model):
    name=models.CharField(max_length=255)
    name_ar=models.CharField(max_length=255)
    short_description=models.TextField()
    short_description_ar=models.TextField()
    long_description=models.TextField()
    long_description_ar=models.TextField()
    price=models.CharField(max_length=255)
    price_ar=models.CharField(max_length=255)
    image=models.ImageField(upload_to=upload_to)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
    
    
class ServiceRequest(models.Model):
    request_code = models.CharField(max_length=255, null=True, blank=True)
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    service = models.ForeignKey(service, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=255, null=True, blank=True)
    address= models.CharField(max_length=255, null=True, blank=True)
    technician= models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='technician', null=True, blank=True)
    request_date = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending')
    priority = models.CharField(max_length=20, null=True, blank=True)
    name= models.CharField(max_length=255)
    phone= models.CharField(max_length=255)
    email= models.CharField(max_length=255)
    last_visit_date = models.DateField(null=True, blank=True)
    
    
    def __str__(self):
        return f"Service Request for {self.service.name}- {self.client.email}"
    

    class Meta:
        ordering = ['-id']
    
class request_report(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    report = models.TextField()
    report_date = models.DateField(auto_now_add=True)
    technician = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='technician_report', null=True, blank=True)
    
    def __str__(self):
        return f"Report for Service Request {self.service_request.id}"
    
    class Meta:
        ordering = ['-id']
    
class request_invoice(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)
    invoice = models.FileField(upload_to=upload_to)
    invoice_date = models.DateField(auto_now_add=True)
    technician = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, related_name='technician_invoice', null=True, blank=True)
    
    def __str__(self):
        return f"Invoice for Service Request {self.service_request.id}"

    class Meta:
        ordering = ['-id']