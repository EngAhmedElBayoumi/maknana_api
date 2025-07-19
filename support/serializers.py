from .models import supportTicket
from rest_framework import serializers

class SupportTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = supportTicket
        fields = ['id', 'name', 'email', 'phone', 'subject', 'message', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']





