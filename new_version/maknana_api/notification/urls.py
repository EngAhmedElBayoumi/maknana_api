from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    # Audit log endpoints
    path('audit-logs/', views.AuditLogListView.as_view(), name='audit-log-list'),
    path('audit-logs/<int:pk>/', views.AuditLogDetailView.as_view(), name='audit-log-detail'),
    
    # Statistics and analytics
    path('statistics/', views.audit_statistics, name='audit-statistics'),
    
    # User activity
    path('user-activity/', views.user_activity, name='current-user-activity'),
    path('user-activity/<str:email>/', views.user_activity, name='user-activity'),
    
    # Model activity
    path('model-activity/<str:model_name>/', views.model_activity, name='model-activity'),
    
    # Testing
    path('test-notification/', views.test_notification, name='test-notification'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
]

