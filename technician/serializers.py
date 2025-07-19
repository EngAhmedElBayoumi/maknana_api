from rest_framework import serializers
from machine_and_factory.models import malfunction_report, malfunction_request, malfunction_invoice
from service.models import request_report, ServiceRequest, request_invoice
from core.models import CustomUser



from rest_framework import serializers
from machine_and_factory.models import malfunction_report, malfunction_request, malfunction_invoice
from service.models import request_report, ServiceRequest, request_invoice
from core.models import CustomUser
from machine_and_factory.serializers import FactorySerializer
# Assuming Machine and MalfunctionType models exist
from machine_and_factory.models import machine, malfunction_type  # Adjust import based on actual model location
from service.models import service  # Adjust import based on actual model location
# Client Serializer (assuming client is a CustomUser or similar)
class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser  # Adjust if client is a different model
        fields = (
            'id',
            'name',
            'email',
            'first_phone',
            'second_phone',
            'type',
            'is_verified',
            'location',
            'photo',
            'is_active',
            'is_staff',
        )

# Machine Serializer (assuming Machine model exists)
class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = machine
        fields = '__all__'


# Service Serializer (for service field in ServiceRequest)
class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = service  # Adjust if model is named differently (e.g., ServiceType)
        fields = '__all__'

# MalfunctionType Serializer (assuming MalfunctionType model exists)
class MalfunctionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = malfunction_type
        fields = '__all__'

# Technician Serializer (unchanged)
class TechnicianSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = (
            'id',
            'name',
            'email',
            'first_phone',
            'second_phone',
            'type',
            'is_verified',
            'location',
            'specialization',
            'photo',
            'is_active',
            'is_staff',
        )

# Malfunction Request Nested Serializer (for use in other serializers)
class MalfunctionRequestNestedSerializer(serializers.ModelSerializer):
    technician = TechnicianSerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    machine = MachineSerializer(read_only=True)
    type = MalfunctionTypeSerializer(read_only=True)
    factory = FactorySerializer(read_only=True)

    class Meta:
        model = malfunction_request
        fields = '__all__'

# Service Request Nested Serializer (for use in other serializers)
class ServiceRequestNestedSerializer(serializers.ModelSerializer):
    technician = TechnicianSerializer(read_only=True)
    class Meta:
        model = ServiceRequest
        fields = '__all__'

# Malfunction Report Serializer
class MalfunctionReportSerializer(serializers.ModelSerializer):
    technician = TechnicianSerializer(read_only=True)
    malfunction_request = MalfunctionRequestNestedSerializer(read_only=True)

    class Meta:
        model = malfunction_report
        fields = '__all__'

# Malfunction Request Serializer (updated for client, machine, type)
class MalfunctionRequestSerializer(serializers.ModelSerializer):
    technician = TechnicianSerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    machine = MachineSerializer(read_only=True)
    type = MalfunctionTypeSerializer(read_only=True)
    factory = FactorySerializer(read_only=True)
    

    class Meta:
        model = malfunction_request
        fields = '__all__'

# Malfunction Invoice Serializer
class MalfunctionInvoiceSerializer(serializers.ModelSerializer):
    technician = TechnicianSerializer(read_only=True)
    malfunction_request = MalfunctionRequestNestedSerializer(read_only=True)

    class Meta:
        model = malfunction_invoice
        fields = '__all__'

class ServiceRequestSerializer(serializers.ModelSerializer):
    technician = TechnicianSerializer(read_only=True)
    client = ClientSerializer(read_only=True)
    service = ServiceSerializer(read_only=True)

    class Meta:
        model = ServiceRequest
        fields = '__all__'

# Request Report Serializer
class RequestReportSerializer(serializers.ModelSerializer):
    technician = TechnicianSerializer(read_only=True)
    service_request = ServiceRequestNestedSerializer(read_only=True, source='request')  # Adjust 'source' if needed

    class Meta:
        model = request_report
        fields = '__all__'

# Request Invoice Serializer
class RequestInvoiceSerializer(serializers.ModelSerializer):
    technician = TechnicianSerializer(read_only=True)
    service_request = ServiceRequestNestedSerializer(read_only=True, source='request')  # Adjust 'source' if needed

    class Meta:
        model = request_invoice
        fields = '__all__'













# class TechnicianSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = (
#             'id',
#             'name',
#             'email',
#             'first_phone',
#             'second_phone',
#             'type',
#             'is_verified',
#             'location',
#             'specialization',
#             'photo',
#             'is_active',
#             'is_staff',
#         )

# class MalfunctionReportSerializer(serializers.ModelSerializer):
#     technician = TechnicianSerializer(read_only=True)
#     class Meta:
#         model = malfunction_report
#         fields = '__all__'

# class MalfunctionRequestSerializer(serializers.ModelSerializer):
#     technician = TechnicianSerializer(read_only=True)
#     class Meta:
#         model = malfunction_request
#         fields = '__all__'

# class MalfunctionInvoiceSerializer(serializers.ModelSerializer):
#     technician = TechnicianSerializer(read_only=True)
#     class Meta:
#         model = malfunction_invoice
#         fields = '__all__'

# class ServiceRequestSerializer(serializers.ModelSerializer):
#     technician = TechnicianSerializer(read_only=True)
#     class Meta:
#         model = ServiceRequest
#         fields = '__all__'

# class RequestReportSerializer(serializers.ModelSerializer):
#     technician = TechnicianSerializer(read_only=True)
#     class Meta:
#         model = request_report
#         fields = '__all__'

# class RequestInvoiceSerializer(serializers.ModelSerializer):
#     technician = TechnicianSerializer(read_only=True)
#     class Meta:
#         model = request_invoice
#         fields = '__all__'
