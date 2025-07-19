from django.db import models
from core.models import CustomUser
from io import BytesIO
from django.core.files import File

import uuid
import os

def upload_to(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4().hex}.{ext}"
    return os.path.join("uploads/images/", filename)
# Create your models here.

class factory(models.Model):
    name= models.CharField(max_length=100)
    location= models.CharField(max_length=100)
    user= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    phone= models.CharField(max_length=100)
    country_code= models.CharField(max_length=100)
    mobile_code= models.CharField(max_length=100)
    responsible_user= models.CharField(max_length=100)
    
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
    

class machine(models.Model):
    name= models.CharField(max_length=100)
    factory= models.ForeignKey(factory, on_delete=models.CASCADE)
    status= models.CharField(max_length=100)
    warranty_status= models.CharField(max_length=100, choices=[('warranty', 'warranty'), ('not warranty', 'not warranty')])
    last_maintenance= models.DateField()
    image= models.ImageField(upload_to=upload_to, null=True, blank=True)
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    catalog= models.FileField(upload_to=upload_to, null=True, blank=True)
    machine_code= models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-id']
    
   
# malfunction type
class malfunction_type(models.Model):
    name= models.CharField(max_length=100)
    description= models.TextField()
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
   
 

# malfunction request
class malfunction_request(models.Model):
    client= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    factory= models.ForeignKey(factory, on_delete=models.CASCADE, null=True, blank=True)
    machine= models.ForeignKey(machine, on_delete=models.CASCADE)
    type= models.ForeignKey(malfunction_type, on_delete=models.CASCADE)
    description= models.TextField()
    file= models.FileField(upload_to=upload_to, null=True, blank=True)
    technician= models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='technician_malfunction_request', blank=True)
    periority= models.CharField(max_length=100, choices=[('low', 'low'), ('medium', 'medium'), ('high', 'high')], default='medium')
    email= models.EmailField(null=True, blank=True)
    phone= models.CharField(max_length=100, null=True, blank=True)
    status= models.CharField(max_length=100, choices=[('pending', 'pending'), ('in progress', 'in progress'), ('completed', 'completed')])
    last_visit= models.DateField(null=True, blank=True)
    
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.machine.name

    class Meta:
        ordering = ['-id']
    
    
class malfunction_report(models.Model):
    malfunction_request= models.ForeignKey(malfunction_request, on_delete=models.CASCADE)
    description= models.TextField()
    file= models.FileField(upload_to=upload_to, null=True, blank=True)
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.malfunction_request.machine.name

    class Meta:
        ordering = ['-id']
    
# malfunction invoice
class malfunction_invoice(models.Model):
    malfunction_request= models.ForeignKey(malfunction_request, on_delete=models.CASCADE)
    description= models.TextField()
    file= models.FileField(upload_to=upload_to, null=True, blank=True)
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.malfunction_request.machine.name

    class Meta:
        ordering = ['-id']
    
# automation request (project_type , machines_number (from-to) ,name , phone , email , date_time)
class automation_request(models.Model):
    client= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Factories complex , machine , factory , workshop,  other
    project_type = models.CharField(max_length=100, choices=[
        ('factory_complex', 'Factory Complex'),
        ('machine', 'Machine'),
        ('factory', 'Factory'), 
        ('workshop', 'Workshop'),
        ('other', 'Other')
    ])
    machines_number = models.CharField(max_length=100)
    name= models.CharField(max_length=100)
    phone= models.CharField(max_length=100)
    email= models.EmailField()
    date_time= models.DateTimeField()
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-id']
    


class market_category(models.Model):
    name= models.CharField(max_length=100)
    description= models.TextField(null=True, blank=True)
    image= models.ImageField(upload_to=upload_to, null=True, blank=True)
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
    
class market_product(models.Model):
    image= models.ImageField(upload_to=upload_to, null=True, blank=True)
    owner=models.ForeignKey(CustomUser, on_delete=models.SET_NULL,blank=True,null=True)
    name= models.CharField(max_length=100)
    description= models.TextField(null=True, blank=True)
    price= models.DecimalField(max_digits=10, decimal_places=2)
    operation_price= models.DecimalField(max_digits=10, decimal_places=2,default=100.00)
    category= models.ForeignKey(market_category, on_delete=models.CASCADE)
    # type new , used
    type= models.CharField(max_length=100, choices=[('new', 'new'), ('used', 'used')])
    # Duration of use
    duration_of_use=models.CharField(max_length=100, null=True, blank=True)
    # warranty status
    warranty_status=models.CharField(max_length=100, choices=[('warranty', 'warranty'), ('not warranty', 'not warranty')] , default='not warranty')
    # factory
    factory=models.ForeignKey(factory, on_delete=models.SET_NULL, null=True, blank=True)
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    sku = models.CharField(max_length=50, null=True, blank=True)  
    quantity = models.PositiveIntegerField(default=0)  
    status = models.CharField(max_length=100, choices=[('available', 'available'), ('out_of_stock', 'out_of_stock')], default='available')  # Added Status
    condition_details = models.TextField(null=True, blank=True)  
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']
    
# order 
class market_order_request(models.Model):
    client= models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product= models.ForeignKey(market_product, on_delete=models.CASCADE)
    quantity= models.IntegerField()
    name= models.CharField(max_length=100)
    phone= models.CharField(max_length=100)
    email= models.EmailField()
    factory_name= models.CharField(max_length=100)
    # address 
    city= models.CharField(max_length=100)
    state= models.CharField(max_length=100)
    address= models.CharField(max_length=100)
    # order status
    status= models.CharField(max_length=100, choices=[('pending', 'pending'), ('in progress', 'in progress'), ('completed', 'completed'), ('canceled', 'canceled')])
    # payment method
    payment_method= models.CharField(max_length=100, choices=[('cash', 'cash'), ('credit card', 'credit card'), ('bank transfer', 'bank transfer')])
    # payment status
    payment_status= models.CharField(max_length=100, choices=[('paid', 'paid'), ('not paid', 'not paid')])
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.product.name
    
    class Meta:
        ordering = ['-id']



# contracts
class Contarct(models.Model):
    client=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    end_date=models.DateField()
    status=models.CharField(max_length=100)
    # المدة
    duration=models.CharField(max_length=100)
    start_from=models.DateField()
    #machine_number
    machine_number=models.CharField(max_length=100)
    factory=models.ForeignKey(factory, on_delete=models.CASCADE)
    # التوقيع
    signature=models.TextField(null=True, blank=True)
    description=models.TextField()
    file=models.FileField(upload_to=upload_to)
    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.code

    class Meta:
        ordering = ['-id']


class shipping_detials(models.Model):
    from_location=models.CharField(max_length=100)
    to_location=models.CharField(max_length=100)
    price=models.DecimalField(max_digits=10, decimal_places=2)

    create_at= models.DateTimeField(auto_now_add=True)
    update_at= models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
    