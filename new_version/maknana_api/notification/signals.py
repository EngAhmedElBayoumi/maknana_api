from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from .models import AuditLog
from .authentication import get_user_from_request
import json
import threading

User = get_user_model()

# Thread-local storage to store the current user
_thread_locals = threading.local()

def get_current_user():
    """Get the current user from thread-local storage."""
    return getattr(_thread_locals, 'user', None)

def set_current_user(user):
    """Set the current user in thread-local storage."""
    _thread_locals.user = user

class AuditMiddleware:
    """Middleware to capture the current user for audit logging."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Use the improved authentication helper
        user = get_user_from_request(request)
        set_current_user(user)
        
        response = self.get_response(request)
        
        # Clear the user after the request
        set_current_user(None)
        
        return response

def get_model_changes(instance, old_instance=None):
    """Compare old and new instance to get changes."""
    changes = {}
    
    if old_instance is None:
        # For creation, all fields are new
        for field in instance._meta.fields:
            field_name = field.name
            value = getattr(instance, field_name)
            if value is not None:
                changes[field_name] = {
                    'old': None,
                    'new': str(value)
                }
    else:
        # For updates, compare old and new values
        for field in instance._meta.fields:
            field_name = field.name
            old_value = getattr(old_instance, field_name)
            new_value = getattr(instance, field_name)
            
            if old_value != new_value:
                changes[field_name] = {
                    'old': str(old_value) if old_value is not None else None,
                    'new': str(new_value) if new_value is not None else None
                }
    
    return changes

@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    """Log model creation and updates."""
    # Skip logging for AuditLog model to avoid infinite recursion
    if sender == AuditLog:
        return
    
    # Skip logging for certain system models
    skip_models = ['Session', 'LogEntry', 'Permission', 'Group', 'ContentType']
    if sender.__name__ in skip_models:
        return
    
    try:
        content_type = ContentType.objects.get_for_model(sender)
        user = get_current_user()
        
        action = 'created' if created else 'updated'
        
        # Get changes
        changes = {}
        if created:
            changes = get_model_changes(instance)
        else:
            # For updates, we need to get the old instance
            # This is a limitation - we can't easily get the old values
            # In a production environment, you might want to use django-simple-history
            # or implement a more sophisticated tracking mechanism
            changes = {'note': 'Updated - old values not tracked in this implementation'}
        
        AuditLog.objects.create(
            user=user,
            action=action,
            content_type=content_type,
            object_id=instance.pk,
            changes=changes,
            model_name=sender.__name__,
            object_repr=str(instance)[:200]
        )
        
        # Send real-time notification (will be implemented in next phase)
        from .utils import send_realtime_notification
        send_realtime_notification({
            'action': action,
            'model': sender.__name__,
            'object_id': instance.pk,
            'user': user.email if user else 'Anonymous',
            'timestamp': AuditLog.objects.filter(
                content_type=content_type,
                object_id=instance.pk
            ).latest('timestamp').timestamp.isoformat(),
            'changes': changes
        })
        
    except Exception as e:
        # Log the error but don't break the original operation
        print(f"Error in audit logging: {e}")

@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    """Log model deletions."""
    # Skip logging for AuditLog model
    if sender == AuditLog:
        return
    
    # Skip logging for certain system models
    skip_models = ['Session', 'LogEntry', 'Permission', 'Group', 'ContentType']
    if sender.__name__ in skip_models:
        return
    
    try:
        content_type = ContentType.objects.get_for_model(sender)
        user = get_current_user()
        
        # Store the instance data before deletion
        changes = {}
        for field in instance._meta.fields:
            field_name = field.name
            value = getattr(instance, field_name)
            if value is not None:
                changes[field_name] = {
                    'old': str(value),
                    'new': None
                }
        
        AuditLog.objects.create(
            user=user,
            action='deleted',
            content_type=content_type,
            object_id=instance.pk,
            changes=changes,
            model_name=sender.__name__,
            object_repr=str(instance)[:200]
        )
        
        # Send real-time notification
        from .utils import send_realtime_notification
        send_realtime_notification({
            'action': 'deleted',
            'model': sender.__name__,
            'object_id': instance.pk,
            'user': user.email if user else 'Anonymous',
            'timestamp': AuditLog.objects.filter(
                content_type=content_type,
                object_id=instance.pk
            ).latest('timestamp').timestamp.isoformat(),
            'changes': changes
        })
        
    except Exception as e:
        # Log the error but don't break the original operation
        print(f"Error in audit logging: {e}")

