# Django Notification System Documentation

## Overview

This documentation describes the comprehensive notification system implemented for the Django REST Framework project. The system tracks all model changes using Django Signals and AuditLog model, with real-time logging capabilities via Pusher integration.

## Features

- **Complete Audit Logging**: Tracks all CREATE, UPDATE, and DELETE operations on any model
- **Real-time Notifications**: Uses Pusher to send real-time notifications to connected clients
- **User Tracking**: Records which user performed each action
- **Change Tracking**: Stores detailed information about what changed
- **REST API**: Provides comprehensive API endpoints for accessing audit data
- **Admin Interface**: Django admin integration for viewing audit logs
- **Dashboard**: Real-time dashboard for monitoring system activity
- **Filtering & Search**: Advanced filtering and search capabilities

## Installation & Setup

### 1. App Installation

The notification app has been created and added to your Django project:

```python
# In project/settings.py
INSTALLED_APPS = [
    # ... other apps
    'notification',
    'django_filters',
]
```

### 2. Middleware Configuration

The AuditMiddleware has been added to capture the current user:

```python
# In project/settings.py
MIDDLEWARE = [
    # ... other middleware
    'notification.signals.AuditMiddleware',
    # ... remaining middleware
]
```

### 3. Pusher Configuration

Pusher credentials are already configured in your settings:

```python
# In project/settings.py
PUSHER_APP_ID = "2008598"
PUSHER_KEY = "cf5338c234a513e939b6"
PUSHER_SECRET = "ad58023a7719d524fbe0"
PUSHER_CLUSTER = "eu"
```

### 4. Database Migration

Run the migrations to create the audit log table:

```bash
python manage.py makemigrations notification
python manage.py migrate
```

## Models

### AuditLog Model

The main model that stores all audit information:

```python
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
```

**Fields:**
- `user`: The user who performed the action (nullable for anonymous actions)
- `action`: Type of action (created, updated, deleted)
- `timestamp`: When the action occurred
- `content_type`: Django ContentType of the affected model
- `object_id`: Primary key of the affected object
- `content_object`: Generic foreign key to the actual object
- `changes`: JSON field containing the changes made
- `model_name`: Name of the model class
- `object_repr`: String representation of the object

## API Endpoints

### Base URL: `/api/notifications/`

### 1. Audit Logs List
- **URL**: `GET /api/notifications/audit-logs/`
- **Description**: List all audit logs with filtering and pagination
- **Authentication**: Required
- **Filters**:
  - `action`: Filter by action type (created, updated, deleted)
  - `model_name`: Filter by model name
  - `user`: Filter by user email
  - `date_from`: Filter from date
  - `date_to`: Filter to date
- **Search**: Search in user email, model name, object representation, and changes
- **Ordering**: By timestamp, action, model_name

**Example Request:**
```bash
GET /api/notifications/audit-logs/?action=created&model_name=service&search=test
```

**Example Response:**
```json
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "user_email": "test@example.com",
            "action": "created",
            "timestamp": "2025-01-07T12:04:26.123456Z",
            "model_name": "service",
            "object_id": 53,
            "object_repr": "Test Service"
        }
    ]
}
```

### 2. Audit Log Detail
- **URL**: `GET /api/notifications/audit-logs/{id}/`
- **Description**: Get detailed information about a specific audit log
- **Authentication**: Required

**Example Response:**
```json
{
    "id": 1,
    "user": 71,
    "user_email": "test@example.com",
    "user_name": "Test User",
    "action": "created",
    "timestamp": "2025-01-07T12:04:26.123456Z",
    "content_type": 15,
    "content_type_name": "service",
    "object_id": 53,
    "changes": {
        "name": {"old": null, "new": "Test Service"},
        "price": {"old": null, "new": "100.00"}
    },
    "model_name": "service",
    "object_repr": "Test Service"
}
```

### 3. Statistics
- **URL**: `GET /api/notifications/statistics/`
- **Description**: Get audit log statistics
- **Authentication**: Required

**Example Response:**
```json
{
    "total_logs": 150,
    "today_logs": 25,
    "week_logs": 89,
    "month_logs": 150,
    "by_action": [
        {"action": "created", "count": 60},
        {"action": "updated", "count": 70},
        {"action": "deleted", "count": 20}
    ],
    "by_model": [
        {"model_name": "service", "count": 45},
        {"model_name": "CustomUser", "count": 30}
    ],
    "recent_activities": [
        {
            "user__email": "test@example.com",
            "action": "created",
            "model_name": "service",
            "object_id": 53,
            "timestamp": "2025-01-07T12:04:26.123456Z",
            "object_repr": "Test Service"
        }
    ]
}
```

### 4. User Activity
- **URL**: `GET /api/notifications/user-activity/`
- **URL**: `GET /api/notifications/user-activity/{email}/`
- **Description**: Get activity logs for current user or specific user
- **Authentication**: Required

### 5. Model Activity
- **URL**: `GET /api/notifications/model-activity/{model_name}/`
- **Description**: Get activity logs for a specific model
- **Authentication**: Required

### 6. Test Notification
- **URL**: `POST /api/notifications/test-notification/`
- **Description**: Send a test real-time notification
- **Authentication**: Required

### 7. Dashboard
- **URL**: `GET /api/notifications/dashboard/`
- **Description**: Render the real-time dashboard
- **Authentication**: Not required (but recommended)

## Real-time Notifications

### Pusher Channels

The system uses three types of Pusher channels:

1. **General Audit Channel**: `audit-channel`
   - Event: `model-change`
   - Receives all model changes

2. **Model-specific Channels**: `model-{model_name}`
   - Event: `change`
   - Receives changes for specific models

3. **User-specific Channels**: `user-{user_email}`
   - Event: `activity`
   - Receives activities for specific users

### Notification Data Format

```json
{
    "action": "created",
    "model": "service",
    "object_id": 53,
    "user": "test@example.com",
    "timestamp": "2025-01-07T12:04:26.123456Z",
    "changes": {
        "name": {"old": null, "new": "Test Service"}
    }
}
```

### Frontend Integration

To receive real-time notifications in your frontend:

```javascript
// Initialize Pusher
const pusher = new Pusher('cf5338c234a513e939b6', {
    cluster: 'eu',
    encrypted: true
});

// Subscribe to general audit channel
const auditChannel = pusher.subscribe('audit-channel');
auditChannel.bind('model-change', function(data) {
    console.log('Model changed:', data);
    // Handle the notification
});

// Subscribe to specific model channel
const serviceChannel = pusher.subscribe('model-service');
serviceChannel.bind('change', function(data) {
    console.log('Service changed:', data);
});

// Subscribe to user-specific channel
const userChannel = pusher.subscribe('user-test@example.com');
userChannel.bind('activity', function(data) {
    console.log('User activity:', data);
});
```

## Dashboard

A real-time dashboard is available at `/api/notifications/dashboard/` that shows:

- Connection status to Pusher
- Real-time statistics
- Live notifications as they happen
- Recent activity feed

The dashboard automatically connects to Pusher and displays notifications in real-time.

## How It Works

### 1. Signal Handling

Django signals are used to automatically capture model changes:

```python
@receiver(post_save)
def log_model_save(sender, instance, created, **kwargs):
    # Create audit log entry
    # Send real-time notification

@receiver(post_delete)
def log_model_delete(sender, instance, **kwargs):
    # Create audit log entry for deletion
    # Send real-time notification
```

### 2. User Tracking

The `AuditMiddleware` captures the current user from the request and stores it in thread-local storage, making it available to the signal handlers.

### 3. Change Tracking

For CREATE operations, all field values are recorded as "new" values.
For UPDATE operations, the system records changes (note: old values are not tracked in this implementation for simplicity).
For DELETE operations, all field values are recorded as "old" values.

### 4. Real-time Notifications

When a model change occurs, the signal handler:
1. Creates an audit log entry
2. Sends a real-time notification via Pusher to multiple channels

## Configuration

### Excluding Models

To exclude certain models from audit logging, modify the signal handlers in `notification/signals.py`:

```python
# Skip logging for certain system models
skip_models = ['Session', 'LogEntry', 'Permission', 'Group', 'ContentType', 'YourModel']
if sender.__name__ in skip_models:
    return
```

### Customizing Notifications

To customize the notification data or channels, modify the `send_realtime_notification` function in `notification/utils.py`.

## Testing

A comprehensive test script is provided at `test_notification_system.py`. Run it to verify the system:

```bash
python test_notification_system.py
```

The test script verifies:
- Audit logging for CREATE, UPDATE, DELETE operations
- Real-time notification sending
- API endpoint functionality

## Admin Interface

The audit logs are available in Django admin at `/admin/notification/auditlog/` with:
- List view with filtering by action, model, timestamp, and user
- Search functionality
- Read-only detailed view
- No add/edit/delete permissions (audit logs should not be modified)

## Security Considerations

1. **Authentication**: All API endpoints require authentication
2. **Read-only**: Audit logs cannot be modified through the API
3. **User Privacy**: User information is limited to email and name
4. **Data Retention**: Consider implementing data retention policies for old audit logs

## Performance Considerations

1. **Database Impact**: Each model operation creates an audit log entry
2. **Pusher Limits**: Be aware of Pusher message limits and pricing
3. **Storage**: Audit logs can grow large over time
4. **Indexing**: Consider adding database indexes for frequently queried fields

## Troubleshooting

### Common Issues

1. **No audit logs created**: Check if the middleware is properly configured
2. **Real-time notifications not working**: Verify Pusher credentials and network connectivity
3. **Permission errors**: Ensure proper authentication for API endpoints

### Debug Mode

Enable debug logging by adding print statements in the signal handlers to see what's being tracked.

## Future Enhancements

Potential improvements for the system:

1. **Old Value Tracking**: Implement proper old value tracking for UPDATE operations
2. **Bulk Operations**: Handle bulk create/update/delete operations
3. **File Changes**: Track file upload/deletion changes
4. **Email Notifications**: Add email notifications for critical changes
5. **Webhooks**: Add webhook support for external integrations
6. **Data Retention**: Implement automatic cleanup of old audit logs
7. **Performance Optimization**: Add caching and optimize database queries

## Conclusion

The notification system provides comprehensive audit logging and real-time notifications for your Django application. It automatically tracks all model changes, provides detailed API access to audit data, and sends real-time notifications to connected clients.

The system is designed to be:
- **Automatic**: No code changes needed for existing models
- **Comprehensive**: Tracks all model operations
- **Real-time**: Immediate notifications via Pusher
- **Secure**: Proper authentication and read-only access
- **Scalable**: Efficient database design and API pagination

For any questions or issues, refer to the test script and this documentation.

