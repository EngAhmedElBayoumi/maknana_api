from django.urls import path
from .views import TechnicianReportsAPIView, TechnicianTasksAPIView, TechnicianInvoicesAPIView

urlpatterns = [
    path('reports/<int:technician_id>/', TechnicianReportsAPIView.as_view(), name='technician-reports'),
    path('tasks/<int:technician_id>/', TechnicianTasksAPIView.as_view(), name='technician-tasks'),
    path('invoices/<int:technician_id>/', TechnicianInvoicesAPIView.as_view(), name='technician-invoices'),
]

