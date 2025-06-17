from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from core.models import CustomUser
from machine_and_factory.models import factory , machine , malfunction_type , malfunction_request  , malfunction_invoice , automation_request , market_category , market_product , market_order_request , Contarct ,shipping_detials
from service.models import service , ServiceRequest , request_report ,request_invoice
import random
from time import sleep


class Command(BaseCommand):
    help = 'Seeds 50 verified users with different types'

    def handle(self, *args, **kwargs):
        #seed_users()

        seed_factories()
        sleep(5)
        print("break 5 second")
        seed_machines()
        sleep(5)
        print("break 5 second")
        seed_malfunctions()
        sleep(5)
        print("break 5 second")
        seed_malfunction_request()
        sleep(5)
        print("break 5 second")
        seed_malfunction_invoice()
        sleep(5)
        print("break 5 second")
        seed_automation_request()
        sleep(5)
        print("break 5 second")
        seed_market_category()
        sleep(5)
        print("break 5 second")
        seed_market_product()
        sleep(5)
        print("break 5 second")
        seed_market_order_request()
        sleep(5)
        print("break 5 second")
        seed_Contarct()
        sleep(5)
        print("break 5 second")
        seed_shipping_detials()
        sleep(5)
        print("break 5 second")
        seed_service()
        sleep(5)
        print("break 5 second")
        seed_ServiceRequest()
        sleep(5)
        print("break 5 second")
        seed_request_report()
        sleep(5)
        print("break 5 second")
        seed_request_invoice()
        print('Seeding completed successfully')
 
 
 
def seed_request_invoice():
    technicians=list(CustomUser.objects.filter(type='technician'))
    for i in range(1,51):
        request_invoice.objects.create(
            service_request=random.choice(ServiceRequest.objects.all()),
            invoice=f'/media/request_invoices/game.png',
            invoice_date=f'2023-01-01',
            technician=random.choice(technicians),
        )
        print(f'request_invoice {i} created')
    print('request_invoice created successfully')
 
 
 
 
# completed function seed_request_report
def seed_request_report():
    technicians = list(CustomUser.objects.filter(type='technician'))
    for i in range(1, 51):
        request_report.objects.create(
            service_request=random.choice(ServiceRequest.objects.all()),
            report=f'report{i}',
            report_date=f'2023-01-01',
            technician=random.choice(technicians),
        )
        print(f'request_report {i} created')
    print('request_report created successfully')

# complted function seed_servicerequest
def seed_ServiceRequest():
    status=['pending', 'accepted', 'rejected']
    clients = list(CustomUser.objects.filter(type='client'))
    technicians = list(CustomUser.objects.filter(type='technician'))
    for i in range(1, 51):
        ServiceRequest.objects.create(
            request_code=f'request code #MLK{i}',
            client=random.choice(clients),
            service=random.choice(service.objects.all()),
            service_type=f'Service type {i}',
            address=f"address {i}",
            technician=random.choice(technicians),
            request_date=f"2023-01-01",
            status=random.choice(status),
            priority=f"priority {i}",
            name=f"name {i}",
            phone=f"0123456789{i}",
            email=f"email{i}@test.dev",
            last_visit_date=f"2023-01-01"
        )
        print(f'ServiceRequest {i} created')
    print('ServiceRequest created successfully')

# complted function seed_service 
def seed_service():
    for i in range(1,51):
        service.objects.create(
            name=f'service {i}',
            name_ar=f'خدمة {i}',
            short_description=f'short description {i}',
            short_description_ar=f'وصف قصير {i}',
            long_description=f'long description {i}',
            long_description_ar=f'وصف طويل {i}',
            price=f'price {i}',
            price_ar=f'سعر {i}',
            image=f'/media/service_images/game.png',
        )
        print(f"service {i} created")
    print('service created successfully')

# completed function  seed_shipping_detials
def seed_shipping_detials():
    for i in range(1,51):
        shipping_detials.objects.create(
            from_location="from city {i}",
            to_location='to city {i}',
            price=random.randint(1, 100),
        )
        print(f"shipping_detials {i},created")
    print('shipping_detials created succfully')
 
# completed function seed_contract
def seed_Contarct():
    for i in range(1, 51):
        clients=list(CustomUser.objects.filter(type='client'))
        Contarct.objects.create(
            client=random.choice(clients),
            code=f'code{i}',
            type=f'type{i}',
            end_date=f'2025-01-01',
            status=f'status{i}',
            duration=f'duration{i}',
            start_from=f'2023-01-01',
            machine_number=f'machine_number{i}',
            factory=random.choice(factory.objects.all()),
            signature=f'signature{i}',
            description=f'description{i}',
            file=f'/media/contracts/game.png',
        )
        print(f'Contarct {i} created')
    print('Contarct created successfully')
 
# completed function seed_market_order_request
def seed_market_order_request():
    status_choice=["pending","in progress","completed","canceled"]
    payment_method_choice=["cash","credit card","bank transfer"]
    payment_status_choice=["paid","not paid"]
    clients=list(CustomUser.objects.filter(type='client'))
    for i in range(1, 51):
        market_order_request.objects.create(
            client=random.choice(clients),
            product=random.choice(market_product.objects.all()),
            quantity=random.randint(1, 100),
            name=f'name{i}',
            phone=f'0101010101{i}',
            email=f'email{i}@testing.dev',
            factory_name=f'factory {i}',
            city=f'city {i}',
            state=f'state {i}',
            address=f'address {i}',
            status=random.choice(status_choice),
            payment_method=random.choice(payment_method_choice),
            payment_status=random.choice(payment_status_choice),
            
        ) 
        print(f'market_order_request {i} created')
    print('market_order_request created successfully')

# completed fuction  seed_market_product
def seed_market_product():
    for i in range(1,51):
        type_choice=["new","used"]
        warranty_status_choice=["warranty","not warranty"]
        market_product.objects.create(
            image=f'/media/malfunction_invoices/game.png',
            owner=random.choice(CustomUser.objects.all()),
            name=f"product {i}",
            description=f"product description {i}",
            price=random.randint(1, 100),
            operation_price=random.randint(1, 100),
            category=random.choice(market_category.objects.all()),
            type=random.choice(type_choice),
            duration_of_use=f"{random.randint(1, 100)} days",
            warranty_status=random.choice(warranty_status_choice),
            factory=random.choice(factory.objects.all()), 
        )   
        print(f"market_product {i} created")
    print('market_product created successfully')
 
# complted function market_category
def seed_market_category():
    for i in range(1,51):
        market_category.objects.create(
            name=f"category {i}",
            description=f"category description {i}",
            image=f'/media/malfunction_invoices/game.png',
        )
        print(f'market_category {i} created')
    print('market_category created successfully')
    
# completed function seed_automation_request
def seed_automation_request():
    clients=list(CustomUser.objects.filter(type='client'))
    for i in range(1, 51):
        automation_request.objects.create(
            client=random.choice(clients),
            project_type=['factory_complex', 'machine', 'factory', 'workshop', 'other'][i % 5],
            machines_number=f'machines_number{i}',
            name=f'name{i}',
            phone=f'0101010101{i}',
            email=f'testing{i}@test.com',
            date_time=f'2025-01-01',
        )
        print(f'automation_request {i} created')
    print('automation_request created successfully')
 
# complted function seed_malfunction_invoice
def seed_malfunction_invoice():
    for i in range(1, 51):
        malfunction_invoice.objects.create(
            malfunction_request=random.choice(malfunction_request.objects.all()),
            description=f'Description{i}',
            file=f'/media/malfunction_invoices/game.png',
        )   
        print(f'Malfunction invoice {i} created')
    print('Malfunction invoices created successfully')
    
# completed function malfunction_request
def seed_malfunction_request():
    status=['pending', 'in progress', 'completed']
    clients = list(CustomUser.objects.filter(type='client'))
    technicians = list(CustomUser.objects.filter(type='technician'))
    for i in range(1, 51):
        malfunction_request.objects.create(
           machine=random.choice(machine.objects.all()),
           description=f'Description{i}',
           file=f'/media/malfunction_requests/game.png',
           email=f'EMAIL@testing.dev',
           phone=f'0101010101{i}',
           type=random.choice(malfunction_type.objects.all()),
           status=status[i % 3],
           client=random.choice(clients),
           technician=random.choice(technicians),
           last_visit=f'2023-01-01',
           
        )
        print(f'Malfunction request {i} created')
    print('Malfunction requests created successfully')

# completed function seed_malfunctions  
def seed_malfunctions():
    for i in range(1, 51):
        malfunction_type.objects.create(
            name=f'Malfunction{i}',
            description=f'Description{i}',
        )
        print(f'Malfunction {i} created')
    print('Malfunctions created successfully')    
        
# completed function seed_machines
def seed_machines():
    warranty_status = ['warranty', 'not warranty']
    for i in range(1, 51):
        machine.objects.create(
            name=f'Machine{i}',
            factory=random.choice(factory.objects.all()),
            status=f'status{i}',
            warranty_status=warranty_status[i % 2],
            last_maintenance=f'2023-01-01',
            image=f'/media/machine_photos/game.png',
            catalog=f'/media/machine_photos/game.png',
            machine_code=f'Mcode{i}',
        )
        print(f'Machine {i} created')
    print('Machines created successfully')
       
# completed function seed_factories
def seed_factories():
    for i in range(1, 51):
        factory.objects.create(
            name=f'Factory{i}',
            location=f'Address{i}',
            user=random.choice(CustomUser.objects.all()),
            phone=f'0101010101{i}',
            country_code=f'+966',
            mobile_code=f'0101010101{i}',
            responsible_user=f'AhmedTest{i}',
        )
        print(f'Factory {i} created')
    print('Factories created successfully')
    
# completed function seed_users
def seed_users():
    for i in range(1, 51):
        CustomUser.objects.create_user(
            name=f'AhmedTest{i}',
            first_phone=f'0101010101{i}',
            second_phone=f'0101010101{i}',
            email=f'AhmedTest{i}9@password.com',
            password=make_password(f'AhmedTest1@password'),
            type=['admin', 'client', 'technician'][i % 3],
            is_verified=True,
            location=f'Address{i}',
            photo=f'/media/user_photos/game.png',
            is_active=True,
            is_staff=False,
            is_superuser=False,
        )
        print(f'User {i} created')
    print('Factories created successfully')