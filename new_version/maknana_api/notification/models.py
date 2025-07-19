from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

User = get_user_model()

class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('created', 'Created'),
        ('updated', 'Updated'),
        ('deleted', 'Deleted'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    changes = models.JSONField(null=True, blank=True)
    model_name = models.CharField(max_length=255, blank=True)
    object_repr = models.CharField(max_length=200, blank=True)

    def __str__(self):
        if self.user:
            return f'{self.user.email} {self.action} {self.model_name} (ID: {self.object_id}) at {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}'
        return f'Anonymous {self.action} {self.model_name} (ID: {self.object_id}) at {self.timestamp.strftime("%Y-%m-%d %H:%M:%S")}'

    class Meta:
        ordering = ['-timestamp']


