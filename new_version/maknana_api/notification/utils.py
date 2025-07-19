import pusher
from django.conf import settings
import json

# Initialize Pusher client
pusher_client = pusher.Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)

def send_realtime_notification(data):
    """Send real-time notification via Pusher."""
    try:
        # Send to a general audit channel
        pusher_client.trigger('audit-channel', 'model-change', data)
        
        # Also send to a model-specific channel
        model_channel = f"model-{data['model'].lower()}"
        pusher_client.trigger(model_channel, 'change', data)
        
        # Send to user-specific channel if user is available
        if data.get('user') and data['user'] != 'Anonymous':
            user_channel = f"user-{data['user']}"
            pusher_client.trigger(user_channel, 'activity', data)
            
        print(f"Real-time notification sent: {data['action']} on {data['model']} by {data['user']}")
        
    except Exception as e:
        print(f"Error sending real-time notification: {e}")

def get_audit_statistics():
    """Get audit log statistics."""
    from .models import AuditLog
    from django.db.models import Count
    from django.utils import timezone
    from datetime import timedelta
    
    now = timezone.now()
    today = now.date()
    week_ago = now - timedelta(days=7)
    month_ago = now - timedelta(days=30)
    
    stats = {
        'total_logs': AuditLog.objects.count(),
        'today_logs': AuditLog.objects.filter(timestamp__date=today).count(),
        'week_logs': AuditLog.objects.filter(timestamp__gte=week_ago).count(),
        'month_logs': AuditLog.objects.filter(timestamp__gte=month_ago).count(),
        'by_action': list(AuditLog.objects.values('action').annotate(count=Count('action'))),
        'by_model': list(AuditLog.objects.values('model_name').annotate(count=Count('model_name')).order_by('-count')[:10]),
        'recent_activities': list(AuditLog.objects.select_related('user').order_by('-timestamp')[:10].values(
            'user__email', 'action', 'model_name', 'object_id', 'timestamp', 'object_repr'
        ))
    }
    
    return stats

