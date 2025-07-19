from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "action",
        "model_name",
        "object_id",
        "timestamp",
    )
    list_filter = ("action", "model_name", "timestamp", "user")
    search_fields = (
        "user__email",
        "model_name",
        "object_id",
        "changes",
    )
    readonly_fields = (
        "user",
        "action",
        "timestamp",
        "content_type",
        "object_id",
        "changes",
        "model_name",
        "object_repr",
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


