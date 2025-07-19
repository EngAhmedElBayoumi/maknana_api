from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Q
from .models import AuditLog
from .serializers import AuditLogSerializer, AuditLogListSerializer
from .utils import get_audit_statistics, send_realtime_notification
import django_filters

class AuditLogFilter(django_filters.FilterSet):
    action = django_filters.ChoiceFilter(choices=AuditLog.ACTION_CHOICES)
    model_name = django_filters.CharFilter(lookup_expr='icontains')
    user = django_filters.CharFilter(field_name='user__email', lookup_expr='icontains')
    date_from = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='gte')
    date_to = django_filters.DateTimeFilter(field_name='timestamp', lookup_expr='lte')
    
    class Meta:
        model = AuditLog
        fields = ['action', 'model_name', 'user', 'date_from', 'date_to']

class AuditLogListView(generics.ListAPIView):
    """List all audit logs with filtering and search capabilities."""
    queryset = AuditLog.objects.select_related('user', 'content_type').all()
    serializer_class = AuditLogListSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AuditLogFilter
    search_fields = ['user__email', 'model_name', 'object_repr', 'changes']
    ordering_fields = ['timestamp', 'action', 'model_name']
    ordering = ['-timestamp']
    permission_classes = [IsAuthenticated]

class AuditLogDetailView(generics.RetrieveAPIView):
    """Retrieve a specific audit log entry."""
    queryset = AuditLog.objects.select_related('user', 'content_type').all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def audit_statistics(request):
    """Get audit log statistics."""
    try:
        stats = get_audit_statistics()
        return Response(stats, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Error retrieving statistics: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_activity(request, email=None):
    """Get activity logs for a specific user or current user."""
    if email is None:
        email = request.user.email
    
    try:
        logs = AuditLog.objects.filter(
            user__email=email
        ).select_related('user', 'content_type').order_by('-timestamp')[:50]
        
        serializer = AuditLogListSerializer(logs, many=True)
        return Response({
            'email': email,
            'activity_count': logs.count(),
            'activities': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Error retrieving user activity: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def model_activity(request, model_name):
    """Get activity logs for a specific model."""
    try:
        logs = AuditLog.objects.filter(
            model_name__icontains=model_name
        ).select_related('user', 'content_type').order_by('-timestamp')[:100]
        
        serializer = AuditLogListSerializer(logs, many=True)
        return Response({
            'model_name': model_name,
            'activity_count': logs.count(),
            'activities': serializer.data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Error retrieving model activity: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def test_notification(request):
    """Test real-time notification system."""
    try:
        test_data = {
            'action': 'test',
            'model': 'TestModel',
            'object_id': 999,
            'user': request.user.email,
            'timestamp': '2025-01-07T12:00:00Z',
            'changes': {'test_field': {'old': 'old_value', 'new': 'new_value'}}
        }
        
        send_realtime_notification(test_data)
        
        return Response({
            'message': 'Test notification sent successfully',
            'data': test_data
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Error sending test notification: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


from django.shortcuts import render
from django.conf import settings

def dashboard(request):
    """Render the audit log dashboard."""
    context = {
        'pusher_key': settings.PUSHER_KEY,
        'pusher_cluster': settings.PUSHER_CLUSTER,
    }
    return render(request, 'notification/dashboard.html', context)

