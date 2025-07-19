from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import factory, machine, malfunction_request, malfunction_report, malfunction_invoice, automation_request, market_category, market_product, market_order_request , malfunction_type , Contarct,shipping_detials
from .serializers import ContractSerializer , ShippingDetialsSerializer
from .serializers import FactorySerializer, MachineSerializer, MalfunctionRequestSerializer, MalfunctionReportSerializer, MalfunctionInvoiceSerializer, AutomationRequestSerializer, MarketCategorySerializer, MarketProductSerializer, MarketOrderRequestSerializer , MalfunctionTypeSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.db.models import Q
from core.utils import get_model_search_fields

import pusher
from django.conf import settings
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import CharField, TextField

# Initialize Pusher
pusher_client = pusher.Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)


class Pagination(PageNumberPagination):
    page_size =10



class MalfunctionTypeViewSet(viewsets.ModelViewSet):
    queryset = malfunction_type.objects.all()
    serializer_class = MalfunctionTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(malfunction_type)

    pusher_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Malfunction Type ID'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Malfunction Type Name'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Malfunction Type Description'),
        }
    )

    @swagger_auto_schema(
        operation_description=(
            "Creates a new malfunction type and triggers a Pusher notification on channel "
            "'malfunction-type-channel' with event 'malfunction-type-created'. "
            "The notification payload includes the created object's ID, name, and description."
        ),
        responses={201: pusher_response_schema}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        instance = serializer.save()
        pusher_client.trigger('malfunction-type-channel', 'malfunction-type-created', {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description
        })

    # update method to trigger Pusher notification
    @swagger_auto_schema(
        operation_description=(
            "Updates an existing malfunction type and triggers a Pusher notification on channel "
            "'malfunction-type-channel' with event 'malfunction-type-updated'. "
            "The notification payload includes the updated object's ID, name, and description."
        ),
        responses={200: pusher_response_schema}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        pusher_client.trigger('malfunction-type-channel', 'malfunction-type-updated', {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description
        })

        return Response(serializer.data)
    
    def perform_update(self, serializer):
        instance = serializer.save()
        pusher_client.trigger('malfunction-type-channel', 'malfunction-type-updated', {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description
        })



class FactoryViewSet(viewsets.ModelViewSet):
    queryset = factory.objects.all()
    serializer_class = FactorySerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = get_model_search_fields(factory)
    pagination_class = Pagination


    @action(detail=False, methods=['get'], url_path='user-factories')
    def user_factories(self, request):
        
        serializer = self.get_serializer(factory.objects.filter(user=request.user), many=True)
        return Response(serializer.data)


#   # pusher notification when a factory is created and updated
    pusher_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Factory ID'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Factory Name'),
            'location': openapi.Schema(type=openapi.TYPE_STRING, description='Factory Location'),
            'user': openapi.Schema(type=openapi.TYPE_INTEGER, description='User ID'),
            'phone': openapi.Schema(type=openapi.TYPE_STRING, description='Factory Phone'),
            'country_code': openapi.Schema(type=openapi.TYPE_STRING, description='Country Code'),
            'mobile_code': openapi.Schema(type=openapi.TYPE_STRING, description='Mobile Code'),
            'responsible_user': openapi.Schema(type=openapi.TYPE_STRING, description='Responsible User'),
        }
    )
    @swagger_auto_schema(
        operation_description=(
            "Creates a new factory and triggers a Pusher notification on channel "
            "'factory-channel' with event 'factory-created'. "
            "The notification payload includes the created object's ID, name, location, user, phone, country code, mobile code, and responsible user."
        ),
        responses={201: pusher_response_schema}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        instance = serializer.save()
        pusher_client.trigger('factory-channel', 'factory-created', {
            'id': instance.id,
            'name': instance.name,
            'location': instance.location,
            'user': instance.user.id,
            'phone': instance.phone,
            'country_code': instance.country_code,
            'mobile_code': instance.mobile_code,
            'responsible_user': instance.responsible_user
        })
    @swagger_auto_schema(
        operation_description=(
            "Updates an existing factory and triggers a Pusher notification on channel "
            "'factory-channel' with event 'factory-updated'. "
            "The notification payload includes the updated object's ID, name, location, user, phone, country code, mobile code, and responsible user."
        ),
        responses={200: pusher_response_schema}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        pusher_client.trigger('factory-channel', 'factory-updated', {
            'id': instance.id,
            'name': instance.name,
            'location': instance.location,
            'user': instance.user.id,
            'phone': instance.phone,
            'country_code': instance.country_code,
            'mobile_code': instance.mobile_code,
            'responsible_user': instance.responsible_user
        })

        return Response(serializer.data)
    def perform_update(self, serializer):
        instance = serializer.save()
        pusher_client.trigger('factory-channel', 'factory-updated', {
            'id': instance.id,
            'name': instance.name,
            'location': instance.location,
            'user': instance.user.id,
            'phone': instance.phone,
            'country_code': instance.country_code,
            'mobile_code': instance.mobile_code,
            'responsible_user': instance.responsible_user
        })
    
    


class MachineViewSet(viewsets.ModelViewSet):
    queryset = machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = get_model_search_fields(machine)
    pagination_class = Pagination

    # user machines
    @action(detail=False, methods=['get'], url_path='user-machines')
    def user_machines(self, request):
        user_machines = machine.objects.filter(factory__user=request.user)
        serializer = self.get_serializer(user_machines, many=True)
        return Response(serializer.data)
    
    
    # machine by factory
    @action(detail=True, methods=['get'], url_path='factory-machines')
    def factory_machines(self, request, pk=None):
        factory_machines = machine.objects.filter(factory_id=pk)
        serializer = self.get_serializer(factory_machines, many=True)
        return Response(serializer.data)

    # pusher notification when a machine is created and updated
    pusher_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Machine ID'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Machine Name'),
            'factory': openapi.Schema(type=openapi.TYPE_INTEGER, description='Factory ID'),
            'status': openapi.Schema(type=openapi.TYPE_STRING, description='Machine Status'),
            'warranty_status': openapi.Schema(type=openapi.TYPE_STRING, description='Warranty Status'),
            'last_maintenance': openapi.Schema(type=openapi.TYPE_STRING, description='Last Maintenance Date'),
            'image': openapi.Schema(type=openapi.TYPE_STRING, description='Image URL'),
            'catalog': openapi.Schema(type=openapi.TYPE_STRING, description='Catalog URL'),
            'machine_code': openapi.Schema(type=openapi.TYPE_STRING, description='Machine Code'),
        }
    )
    @swagger_auto_schema(
        operation_description=(
            "Creates a new machine and triggers a Pusher notification on channel "
            "'machine-channel' with event 'machine-created'. "
            "The notification payload includes the created object's ID, name, factory, status, warranty status, last maintenance date, image URL, catalog URL, and machine code."
        ),
        responses={201: pusher_response_schema}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        instance = serializer.save()
        pusher_client.trigger('machine-channel', 'machine-created', {
            'id': instance.id,
            'name': instance.name,
            'factory': instance.factory.id,
            'status': instance.status,
            'warranty_status': instance.warranty_status,
            'last_maintenance': instance.last_maintenance.isoformat(),
            'image': request.build_absolute_uri(instance.image.url) if instance.image else None,
            'catalog': request.build_absolute_uri(instance.catalog.url) if instance.catalog else None,
            'machine_code': instance.machine_code
        })
    @swagger_auto_schema(
        operation_description=(
            "Updates an existing machine and triggers a Pusher notification on channel "
            "'machine-channel' with event 'machine-updated'. "
            "The notification payload includes the updated object's ID, name, factory, status, warranty status, last maintenance date, image URL, catalog URL, and machine code."
        ),
        responses={200: pusher_response_schema}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        pusher_client.trigger('machine-channel', 'machine-updated', {
            'id': instance.id,
            'name': instance.name,
            'factory': instance.factory.id,
            'status': instance.status,
            'warranty_status': instance.warranty_status,
            'last_maintenance': instance.last_maintenance.isoformat(),
            'image': request.build_absolute_uri(instance.image.url) if instance.image else None,
            'catalog': request.build_absolute_uri(instance.catalog.url) if instance.catalog else None,
            'machine_code': instance.machine_code
        })

        return Response(serializer.data)

    def perform_update(self, serializer):
        instance = serializer.save()
        pusher_client.trigger('machine-channel', 'machine-updated', {
            'id': instance.id,
            'name': instance.name,
            'factory': instance.factory.id,
            'status': instance.status,
            'warranty_status': instance.warranty_status,
            'last_maintenance': instance.last_maintenance.isoformat(),
            'image': request.build_absolute_uri(instance.image.url) if instance.image else None,
            'catalog': request.build_absolute_uri(instance.catalog.url) if instance.catalog else None,
            'machine_code': instance.machine_code
        })






# class MalfunctionRequestViewSet(viewsets.ModelViewSet):
#     queryset = malfunction_request.objects.all()
#     serializer_class = MalfunctionRequestSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     pagination_class = Pagination
#     search_fields = get_model_search_fields(malfunction_request)

#     @action(detail=False, methods=['get'])
#     def client_requests(self, request):
#         client_requests = self.queryset.filter(client=request.user)
#         serializer = self.get_serializer(client_requests, many=True)
#         return Response(serializer.data)

#     @action(detail=False, methods=['get'])
#     def technician_requests(self, request):
#         technician_requests = self.queryset.filter(technician=request.user)
#         serializer = self.get_serializer(technician_requests, many=True)
#         return Response(serializer.data)


#     # pusher notification when a malfunction request is created and updated (when assigning a technician notificate the client and the technician)
#     pusher_response_schema = openapi.Schema(
#         type=openapi.TYPE_OBJECT,
#         properties={
#             'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Malfunction Request ID'),
#             'client': openapi.Schema(type=openapi.TYPE_INTEGER, description='Client ID'),
#             'factory': openapi.Schema(type=openapi.TYPE_INTEGER, description='Factory ID'),
#             'machine': openapi.Schema(type=openapi.TYPE_INTEGER, description='Machine ID'),
#             'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='Malfunction Type ID'),
#             'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
#             'file': openapi.Schema(type=openapi.TYPE_STRING, description='File URL'),
#             'technician': openapi.Schema(type=openapi.TYPE_INTEGER, description='Technician ID'),
#         }
#     )
#     @swagger_auto_schema(
#         operation_description=(
#             "Creates a new malfunction request and triggers a Pusher notification on channel "
#             "'malfunction-request-channel' with event 'malfunction-request-created'. "
#             "The notification payload includes the created object's ID, client, factory, machine, type, description, file URL, and technician."
#         ),
#         responses={201: pusher_response_schema}
#     )
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         self.perform_create(serializer)
#         headers = self.get_success_headers(serializer.data)
#         return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class MalfunctionRequestViewSet(viewsets.ModelViewSet):
    queryset = malfunction_request.objects.all()
    serializer_class = MalfunctionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(malfunction_request)

    # ================= Custom Actions =================
    @action(detail=False, methods=['get'])
    def client_requests(self, request):
        client_requests = self.queryset.filter(client=request.user)
        serializer = self.get_serializer(client_requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def technician_requests(self, request):
        technician_requests = self.queryset.filter(technician=request.user)
        serializer = self.get_serializer(technician_requests, many=True)
        return Response(serializer.data)

    # ================= Schema for Pusher =================
    pusher_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Malfunction Request ID'),
            'client': openapi.Schema(type=openapi.TYPE_INTEGER, description='Client ID'),
            'factory': openapi.Schema(type=openapi.TYPE_INTEGER, description='Factory ID'),
            'machine': openapi.Schema(type=openapi.TYPE_INTEGER, description='Machine ID'),
            'type': openapi.Schema(type=openapi.TYPE_INTEGER, description='Malfunction Type ID'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
            'file': openapi.Schema(type=openapi.TYPE_STRING, description='File URL'),
            'technician': openapi.Schema(type=openapi.TYPE_INTEGER, description='Technician ID'),
        }
    )

    # ================= Create =================
    @swagger_auto_schema(
        operation_description=(
            "Creates a new malfunction request and triggers a Pusher notification on channel "
            "'user-<user_id>' for both client and technician (if assigned)."
        ),
        responses={201: pusher_response_schema}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        instance = self.queryset.get(id=serializer.data['id'])  # fetch created instance
        data = serializer.data

        # Notify client
        if instance.client:
            pusher_client.trigger(f'user-{instance.client.id}', 'malfunction-request-created', data)

        # Notify technician (if assigned)
        if instance.technician:
            pusher_client.trigger(f'user-{instance.technician.id}', 'malfunction-request-created', data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    # ================= Update =================
    @swagger_auto_schema(
        operation_description=(
            "Updates a malfunction request and notifies client and technician (if assigned) "
            "on their private Pusher channels 'user-<id>' with event 'malfunction-request-updated'."
        ),
        responses={200: pusher_response_schema}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        data = serializer.data

        # Notify client
        if instance.client:
            pusher_client.trigger(f'user-{instance.client.id}', 'malfunction-request-updated', data)

        # Notify technician (if assigned)
        if instance.technician:
            pusher_client.trigger(f'user-{instance.technician.id}', 'malfunction-request-updated', data)

        return Response(data) 
    



# class MalfunctionReportViewSet(viewsets.ModelViewSet):
#     queryset = malfunction_report.objects.all()
#     serializer_class = MalfunctionReportSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     pagination_class = Pagination
#     search_fields = get_model_search_fields(malfunction_report)



class MalfunctionReportViewSet(viewsets.ModelViewSet):
    queryset = malfunction_report.objects.all()
    serializer_class = MalfunctionReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(malfunction_report)

    pusher_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Report ID'),
            'malfunction_request': openapi.Schema(type=openapi.TYPE_INTEGER, description='Request ID'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
            'file': openapi.Schema(type=openapi.TYPE_STRING, description='File URL'),
        }
    )

    @swagger_auto_schema(
        operation_description=(
            "Creates a malfunction report and notifies the related client and technician "
            "on Pusher channels 'user-<id>' with event 'malfunction-report-created'."
        ),
        responses={201: pusher_response_schema}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        report = self.queryset.get(id=serializer.data['id'])
        request_instance = report.malfunction_request
        data = serializer.data

        # Notify client
        if request_instance.client:
            pusher_client.trigger(f'user-{request_instance.client.id}', 'malfunction-report-created', data)

        # Notify technician
        if request_instance.technician:
            pusher_client.trigger(f'user-{request_instance.technician.id}', 'malfunction-report-created', data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_description=(
            "Updates a malfunction report and notifies the related client and technician "
            "on Pusher channels 'user-<id>' with event 'malfunction-report-updated'."
        ),
        responses={200: pusher_response_schema}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        request_instance = instance.malfunction_request
        data = serializer.data

        # Notify client
        if request_instance.client:
            pusher_client.trigger(f'user-{request_instance.client.id}', 'malfunction-report-updated', data)

        # Notify technician
        if request_instance.technician:
            pusher_client.trigger(f'user-{request_instance.technician.id}', 'malfunction-report-updated', data)

        return Response(data)

# class MalfunctionInvoiceViewSet(viewsets.ModelViewSet):
#     queryset = malfunction_invoice.objects.all()
#     serializer_class = MalfunctionInvoiceSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     pagination_class = Pagination
#     search_fields = get_model_search_fields(malfunction_invoice)




class MalfunctionInvoiceViewSet(viewsets.ModelViewSet):
    queryset = malfunction_invoice.objects.all()
    serializer_class = MalfunctionInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(malfunction_invoice)

    # Pusher response schema for documentation
    pusher_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Invoice ID'),
            'malfunction_request': openapi.Schema(type=openapi.TYPE_INTEGER, description='Request ID'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Description'),
            'file': openapi.Schema(type=openapi.TYPE_STRING, description='File URL'),
        }
    )

    @swagger_auto_schema(
        operation_description=(
            "Creates a malfunction invoice and sends Pusher notifications to the client and technician "
            "on channels 'user-<id>' with event 'malfunction-invoice-created'."
        ),
        responses={201: pusher_response_schema}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        invoice = self.queryset.get(id=serializer.data['id'])
        request_instance = invoice.malfunction_request
        data = serializer.data

        # Notify client
        if request_instance.client:
            pusher_client.trigger(f'user-{request_instance.client.id}', 'malfunction-invoice-created', data)

        # Notify technician
        if request_instance.technician:
            pusher_client.trigger(f'user-{request_instance.technician.id}', 'malfunction-invoice-created', data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_description=(
            "Updates a malfunction invoice and sends Pusher notifications to the client and technician "
            "on channels 'user-<id>' with event 'malfunction-invoice-updated'."
        ),
        responses={200: pusher_response_schema}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        request_instance = instance.malfunction_request
        data = serializer.data

        # Notify client
        if request_instance.client:
            pusher_client.trigger(f'user-{request_instance.client.id}', 'malfunction-invoice-updated', data)

        # Notify technician
        if request_instance.technician:
            pusher_client.trigger(f'user-{request_instance.technician.id}', 'malfunction-invoice-updated', data)

        return Response(data)


class AutomationRequestViewSet(viewsets.ModelViewSet):
    queryset = automation_request.objects.all()
    serializer_class = AutomationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(automation_request)

    @action(detail=False, methods=['get'], url_path='client-requests')
    def client_requests(self, request):
        client_requests = self.queryset.filter(client=request.user)
        serializer = self.get_serializer(client_requests, many=True)
        return Response(serializer.data)

    pusher_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'client': openapi.Schema(type=openapi.TYPE_INTEGER),
            'project_type': openapi.Schema(type=openapi.TYPE_STRING),
            'machines_number': openapi.Schema(type=openapi.TYPE_STRING),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'phone': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'date_time': openapi.Schema(type=openapi.TYPE_STRING, format='date-time'),
        }
    )

    @swagger_auto_schema(
        operation_description="""
Create a new automation request.

📢 **Pusher Notification**

- **Channel**: `admin-channel`
- **Event**: `automation-request-created`

Sent to notify admins that a new automation request has been submitted.
""",
        responses={201: pusher_response_schema}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        instance = self.queryset.get(id=serializer.data['id'])
        data = serializer.data

        pusher_client.trigger('admin-channel', 'automation-request-created', data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_description="""
Update an existing automation request.

📢 **Pusher Notification**

- **Channel**: `user-<client_id>`
- **Event**: `automation-request-updated`

Notifies the client that their automation request has been modified.
""",
        responses={200: pusher_response_schema}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        data = serializer.data

        if instance.client:
            pusher_client.trigger(f'user-{instance.client.id}', 'automation-request-updated', data)

        return Response(data)

class MarketCategoryViewSet(viewsets.ModelViewSet):
    queryset = market_category.objects.all()
    serializer_class = MarketCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(market_category)

    # pusher notification when a market category is created and updated
    pusher_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Category Name'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Category Description'),
        }
    )
    @swagger_auto_schema(
        operation_description=(
            "Creates a new market category and triggers a Pusher notification on channel "
            "'market-category-channel' with event 'market-category-created'. "
            "The notification payload includes the created object's ID, name, and description."
        ),
        responses={201: pusher_response_schema}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        instance = serializer.save()
        pusher_client.trigger('market-category-channel', 'market-category-created', {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description
        })
    @swagger_auto_schema(
        operation_description=(
            "Updates an existing market category and triggers a Pusher notification on channel "
            "'market-category-channel' with event 'market-category-updated'. "
            "The notification payload includes the updated object's ID, name, and description."
        ),
        responses={200: pusher_response_schema}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        pusher_client.trigger('market-category-channel', 'market-category-updated', {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description
        })

        return Response(serializer.data)
    def perform_update(self, serializer):
        instance = serializer.save()
        pusher_client.trigger('market-category-channel', 'market-category-updated', {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description
        })
    


class MarketProductViewSet(viewsets.ModelViewSet):
    queryset = market_product.objects.all()
    serializer_class = MarketProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(market_product)

    # filter by type new or used
    def get_queryset(self):
        category_id = self.request.query_params.get('category')
        if category_id:
            return self.queryset.filter(category_id=category_id)
        return self.queryset


    @action(detail=False, methods=['get'], url_path='new-products')
    def new_products(self, request):
        """
        Retrieve a list of new products.

        Query Parameters:
            category (integer): Filter products by category ID
                example: 1

        Responses:
            200:
                description: List of new products
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                $ref: "#/components/schemas/MarketProduct"
        """
        category_id = self.request.query_params.get('category')
        new_products = self.queryset.filter(type='new')
        if category_id:
            new_products = new_products.filter(category_id=category_id)
        serializer = self.get_serializer(new_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='used-products')
    def used_products(self, request):
        """
        Retrieve a list of used products.

        Query Parameters:
            category (integer): Filter products by category ID
                example: 1

        Responses:
            200:
                description: List of used products
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                $ref: "#/components/schemas/MarketProduct"
        """
        category_id = self.request.query_params.get('category')
        used_products = self.queryset.filter(type='used')
        if category_id:
            used_products = used_products.filter(category_id=category_id)
        serializer = self.get_serializer(used_products, many=True)
        return Response(serializer.data)

    # pusher notification when a market product is created and updated
    pusher_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER, description='Product ID'),
            'name': openapi.Schema(type=openapi.TYPE_STRING, description='Product Name'),
            'category': openapi.Schema(type=openapi.TYPE_INTEGER, description='Category ID'),
            'type': openapi.Schema(type=openapi.TYPE_STRING, description='Product Type (new/used)'),
            'price': openapi.Schema(type=openapi.TYPE_NUMBER, format='float', description='Product Price'),
            'description': openapi.Schema(type=openapi.TYPE_STRING, description='Product Description'),
            'image': openapi.Schema(type=openapi.TYPE_STRING, description='Image URL'),
        }
    )
    @swagger_auto_schema(
        operation_description=(
            "Creates a new market product and triggers a Pusher notification on channel "
            "'market-product-channel' with event 'market-product-created'. "
            "The notification payload includes the created object's ID, name, category, type, price, description, and image URL."
        ),
        responses={201: pusher_response_schema}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    def perform_create(self, serializer):
        instance = serializer.save()
        pusher_client.trigger('market-product-channel', 'market-product-created', {
            'id': instance.id,
            'name': instance.name,
            'category': instance.category.id,
            'type': instance.type,
            'price': str(instance.price),
            'description': instance.description,
            'image': request.build_absolute_uri(instance.image.url) if instance.image else None
        })
    @swagger_auto_schema(
        operation_description=(
            "Updates an existing market product and triggers a Pusher notification on channel "
            "'market-product-channel' with event 'market-product-updated'. "
            "The notification payload includes the updated object's ID, name, category, type, price, description, and image URL."
        ),
        responses={200: pusher_response_schema}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        pusher_client.trigger('market-product-channel', 'market-product-updated', {
            'id': instance.id,
            'name': instance.name,
            'category': instance.category.id,
            'type': instance.type,
            'price': str(instance.price),
            'description': instance.description,
            'image': request.build_absolute_uri(instance.image.url) if instance.image else None
        })

        return Response(serializer.data)
    def perform_update(self, serializer):
        instance = serializer.save()
        pusher_client.trigger('market-product-channel', 'market-product-updated', {
            'id': instance.id,
            'name': instance.name,
            'category': instance.category.id,
            'type': instance.type,
            'price': str(instance.price),
            'description': instance.description,
            'image': request.build_absolute_uri(instance.image.url) if instance.image else None
        })
    



class MarketOrderRequestViewSet(viewsets.ModelViewSet):
    queryset = market_order_request.objects.all()
    serializer_class = MarketOrderRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(market_order_request)

    # ========== Client Orders ==========
    @action(detail=False, methods=['get'], url_path='client-orders')
    def client_orders(self, request):
        client_orders = self.queryset.filter(client=request.user)
        serializer = self.get_serializer(client_orders, many=True)
        return Response(serializer.data)

    # ========== Pusher Response Schema for Docs ==========
    pusher_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'client': openapi.Schema(type=openapi.TYPE_INTEGER),
            'product': openapi.Schema(type=openapi.TYPE_INTEGER),
            'quantity': openapi.Schema(type=openapi.TYPE_INTEGER),
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'phone': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'factory_name': openapi.Schema(type=openapi.TYPE_STRING),
            'city': openapi.Schema(type=openapi.TYPE_STRING),
            'state': openapi.Schema(type=openapi.TYPE_STRING),
            'address': openapi.Schema(type=openapi.TYPE_STRING),
            'status': openapi.Schema(type=openapi.TYPE_STRING),
            'payment_method': openapi.Schema(type=openapi.TYPE_STRING),
            'payment_status': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )

    # ========== Create ==========
    @swagger_auto_schema(
        operation_description="""
Creates a new market order.

📢 **Pusher Notification**

- **Channel**: `admin-channel`
- **Event**: `market-order-created`

This notifies the admin that a new order has been placed.
""",
        responses={201: pusher_response_schema}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        instance = self.queryset.get(id=serializer.data['id'])
        data = serializer.data

        # 🔔 Notify Admin
        pusher_client.trigger('admin-channel', 'market-order-created', data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    # ========== Update ==========
    @swagger_auto_schema(
        operation_description="""
Updates an existing market order.

📢 **Pusher Notification**

- **Channel**: `user-<client_id>`
- **Event**: `market-order-updated`

This notifies the client about updates to their order.
""",
        responses={200: pusher_response_schema}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        data = serializer.data

        # 🔔 Notify Client
        if instance.client:
            pusher_client.trigger(f'user-{instance.client.id}', 'market-order-updated', data)

        return Response(data)


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contarct.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'type', 'status', 'duration', 'machine_number', 'description']

    # ========= Filtering contracts by factory if passed in query params =========
    def get_queryset(self):
        queryset = super().get_queryset()
        factory_id = self.request.query_params.get('factory')
        if factory_id:
            queryset = queryset.filter(factory_id=factory_id)
        return queryset

    # ========= Get authenticated user's contracts =========
    @action(detail=False, methods=['get'])
    def user_contracts(self, request):
        """
        Get all contracts for the authenticated user.
        """
        contracts = self.queryset.filter(client=request.user)
        page = self.paginate_queryset(contracts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(contracts, many=True)
        return Response(serializer.data)

    # ========= Swagger schema for contract notifications =========
    pusher_response_schema = openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
            'client': openapi.Schema(type=openapi.TYPE_INTEGER),
            'code': openapi.Schema(type=openapi.TYPE_STRING),
            'type': openapi.Schema(type=openapi.TYPE_STRING),
            'status': openapi.Schema(type=openapi.TYPE_STRING),
            'duration': openapi.Schema(type=openapi.TYPE_STRING),
            'start_from': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'end_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
            'machine_number': openapi.Schema(type=openapi.TYPE_STRING),
            'factory': openapi.Schema(type=openapi.TYPE_INTEGER),
            'signature': openapi.Schema(type=openapi.TYPE_STRING),
            'description': openapi.Schema(type=openapi.TYPE_STRING),
            'file': openapi.Schema(type=openapi.TYPE_STRING),
        }
    )

    # ========= Create =========
    @swagger_auto_schema(
        operation_description="""
Create a new contract.

📢 **Pusher Notification**

- **Channel**: `admin-channel`
- **Event**: `contract-created`

This notifies the admin when a new contract is added.
""",
        responses={201: pusher_response_schema}
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        contract = self.queryset.get(id=serializer.data['id'])
        data = serializer.data

        # 🔔 Notify Admin
        pusher_client.trigger('admin-channel', 'contract-created', data)

        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    # ========= Update =========
    @swagger_auto_schema(
        operation_description="""
Update an existing contract.

📢 **Pusher Notification**

- **Channel**: `user-<client_id>`
- **Event**: `contract-updated`

This notifies the contract owner (client) when the contract is edited.
""",
        responses={200: pusher_response_schema}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        data = serializer.data

        # 🔔 Notify Client
        if instance.client:
            pusher_client.trigger(f'user-{instance.client.id}', 'contract-updated', data)

        return Response(data)


class ShippingDetialsViewSet(viewsets.ModelViewSet):
    queryset = shipping_detials.objects.all()
    serializer_class = ShippingDetialsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(shipping_detials)

    # action get price depend on from and to
    @action(detail=False, methods=['get'], url_path='get-price')
    def get_price(self, request):
        from_country = request.query_params.get('from')
        to_country = request.query_params.get('to')
        if from_country and to_country:
            shipping = shipping_detials.objects.filter(from_country=from_country, to_country=to_country).first()
            if shipping:
                return Response({'price': shipping.price})
            else:
                return Response({'error': 'Shipping details not found'}, status=404)
        else:
            return Response({'error': 'From and To countries are required'}, status=400)



                

    