from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServiceViewSet, ClientRequestView, AdminRequestView, TechnicianRequestView

router = DefaultRouter()
router.register(r'services', ServiceViewSet, basename='service')

urlpatterns = [
    path('', include(router.urls)),
    path('client/request/', ClientRequestView.as_view(), name='client-request'),
    path('admin/request/', AdminRequestView.as_view(), name='admin-request'),
    path('admin/request/<int:pk>/', AdminRequestView.as_view(), name='admin-request-detail'),
    path('technician/request/', TechnicianRequestView.as_view(), name='technician-request'),
]