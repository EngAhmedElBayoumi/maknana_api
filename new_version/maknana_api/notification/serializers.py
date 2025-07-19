from rest_framework import serializers
from .models import AuditLog
from django.contrib.auth import get_user_model

User = get_user_model()

class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_name = serializers.CharField(source='user.name', read_only=True)
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id',
            'user',
            'user_email',
            'user_name',
            'action',
            'timestamp',
            'content_type',
            'content_type_name',
            'object_id',
            'changes',
            'model_name',
            'object_repr'
        ]
        read_only_fields = fields
    
    def get_user_full_name(self, obj):
        if obj.user:
            return obj.user.name or obj.user.email
        return "Anonymous"

class AuditLogListSerializer(serializers.ModelSerializer):
    """Simplified serializer for list views."""
    user_email = serializers.SerializerMethodField()
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditLog
        fields = [
            'id',
            'user_email',
            'user_name',
            'action',
            'timestamp',
            'model_name',
            'object_id',
            'object_repr'
        ]
        read_only_fields = fields
    
    def get_user_email(self, obj):
        return obj.user.email if obj.user else None
    
    def get_user_name(self, obj):
        return obj.user.name if obj.user else None

