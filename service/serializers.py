from rest_framework import serializers
from .models import service, ServiceRequest

class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = service
        fields = '__all__'

class ServiceRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceRequest
        fields = '__all__'
        extra_kwargs = {
            field.name: {'required': not field.null} for field in model._meta.fields
        }
        
    # represnt all service detials in the service request
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['service'] = ServiceSerializer(instance.service).data
        
        return representation