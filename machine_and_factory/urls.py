# filepath: d:\windows_backup-13-01-2025\Abd_elrahman\maknana_api\machine_and_factory\urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FactoryViewSet, MachineViewSet, MalfunctionRequestViewSet, MalfunctionReportViewSet, MalfunctionInvoiceViewSet, AutomationRequestViewSet
from .views import MarketCategoryViewSet, MarketProductViewSet, MarketOrderRequestViewSet , MalfunctionTypeViewSet , ContractViewSet , ShippingDetialsViewSet

router = DefaultRouter()
router.register(r'factories', FactoryViewSet, basename='factory')
router.register(r'machines', MachineViewSet, basename='machine')
router.register(r'malfunction_requests', MalfunctionRequestViewSet, basename='malfunction_request')
router.register(r'malfunction_reports', MalfunctionReportViewSet, basename='malfunction_report')
router.register(r'malfunction_invoices', MalfunctionInvoiceViewSet, basename='malfunction_invoice')
router.register(r'automation_requests', AutomationRequestViewSet, basename='automation_request')
router.register(r'market_categories', MarketCategoryViewSet, basename='market_category')
router.register(r'market_products', MarketProductViewSet, basename='market_product')
router.register(r'market_order_requests', MarketOrderRequestViewSet, basename='market_order_request')
router.register(r'malfunction_types', MalfunctionTypeViewSet, basename='malfunction_type')
router.register('contracts', ContractViewSet, basename='contract')
router.register('shipping_details', ShippingDetialsViewSet, basename='shipping_details')

urlpatterns = [
    path('', include(router.urls)),
]