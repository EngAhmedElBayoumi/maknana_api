from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import factory, machine, malfunction_request, malfunction_report, malfunction_invoice, automation_request, market_category, market_product, market_order_request , malfunction_type , Contarct,shipping_detials
from .serializers import ContractSerializer , ShippingDetialsSerializer
from .serializers import FactorySerializer, MachineSerializer, MalfunctionRequestSerializer, MalfunctionReportSerializer, MalfunctionInvoiceSerializer, AutomationRequestSerializer, MarketCategorySerializer, MarketProductSerializer, MarketOrderRequestSerializer , MalfunctionTypeSerializer
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from django.db.models import Q
from core.utils import get_model_search_fields

class Pagination(PageNumberPagination):
    page_size = 10



class MalfunctionTypeViewSet(viewsets.ModelViewSet):
    queryset = malfunction_type.objects.all()
    serializer_class = MalfunctionTypeSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(malfunction_type)
    


class FactoryViewSet(viewsets.ModelViewSet):
    queryset = factory.objects.all()
    serializer_class = FactorySerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = get_model_search_fields(factory)
    pagination_class = Pagination


    @action(detail=False, methods=['get'], url_path='user-factories')
    def user_factories(self, request):
        
        serializer = self.get_serializer(factory.objects.filter(user=request.user), many=True)
        return Response(serializer.data)

class MachineViewSet(viewsets.ModelViewSet):
    queryset = machine.objects.all()
    serializer_class = MachineSerializer
    permission_classes = [permissions.IsAuthenticated]
    search_fields = get_model_search_fields(machine)
    pagination_class = Pagination

    # user machines
    @action(detail=False, methods=['get'], url_path='user-machines')
    def user_machines(self, request):
        user_machines = machine.objects.filter(factory__user=request.user)
        serializer = self.get_serializer(user_machines, many=True)
        return Response(serializer.data)
    
    
    # machine by factory
    @action(detail=True, methods=['get'], url_path='factory-machines')
    def factory_machines(self, request, pk=None):
        factory_machines = machine.objects.filter(factory_id=pk)
        serializer = self.get_serializer(factory_machines, many=True)
        return Response(serializer.data)

class MalfunctionRequestViewSet(viewsets.ModelViewSet):
    queryset = malfunction_request.objects.all()
    serializer_class = MalfunctionRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(malfunction_request)

    @action(detail=False, methods=['get'])
    def client_requests(self, request):
        client_requests = self.queryset.filter(client=request.user)
        serializer = self.get_serializer(client_requests, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def technician_requests(self, request):
        technician_requests = self.queryset.filter(technician=request.user)
        serializer = self.get_serializer(technician_requests, many=True)
        return Response(serializer.data)

class MalfunctionReportViewSet(viewsets.ModelViewSet):
    queryset = malfunction_report.objects.all()
    serializer_class = MalfunctionReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(malfunction_report)

class MalfunctionInvoiceViewSet(viewsets.ModelViewSet):
    queryset = malfunction_invoice.objects.all()
    serializer_class = MalfunctionInvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(malfunction_invoice)

class AutomationRequestViewSet(viewsets.ModelViewSet):
    queryset = automation_request.objects.all()
    serializer_class = AutomationRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(automation_request)

    @action(detail=False, methods=['get'], url_path='client-requests')
    def client_requests(self, request):
        client_requests = self.queryset.filter(client=request.user)
        serializer = self.get_serializer(client_requests, many=True)
        return Response(serializer.data)

class MarketCategoryViewSet(viewsets.ModelViewSet):
    queryset = market_category.objects.all()
    serializer_class = MarketCategorySerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(market_category)

class MarketProductViewSet(viewsets.ModelViewSet):
    queryset = market_product.objects.all()
    serializer_class = MarketProductSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(market_product)

    # filter by type new or used
    def get_queryset(self):
        category_id = self.request.query_params.get('category')
        if category_id:
            return self.queryset.filter(category_id=category_id)
        return self.queryset


    @action(detail=False, methods=['get'], url_path='new-products')
    def new_products(self, request):
        """
        Retrieve a list of new products.

        Query Parameters:
            category (integer): Filter products by category ID
                example: 1

        Responses:
            200:
                description: List of new products
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                $ref: "#/components/schemas/MarketProduct"
        """
        category_id = self.request.query_params.get('category')
        new_products = self.queryset.filter(type='new')
        if category_id:
            new_products = new_products.filter(category_id=category_id)
        serializer = self.get_serializer(new_products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='used-products')
    def used_products(self, request):
        """
        Retrieve a list of used products.

        Query Parameters:
            category (integer): Filter products by category ID
                example: 1

        Responses:
            200:
                description: List of used products
                content:
                    application/json:
                        schema:
                            type: array
                            items:
                                $ref: "#/components/schemas/MarketProduct"
        """
        category_id = self.request.query_params.get('category')
        used_products = self.queryset.filter(type='used')
        if category_id:
            used_products = used_products.filter(category_id=category_id)
        serializer = self.get_serializer(used_products, many=True)
        return Response(serializer.data)

class MarketOrderRequestViewSet(viewsets.ModelViewSet):
    queryset = market_order_request.objects.all()
    serializer_class = MarketOrderRequestSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(market_order_request)


    @action(detail=False, methods=['get'], url_path='client-orders')
    def client_orders(self, request):
        client_orders = self.queryset.filter(client=request.user)
        serializer = self.get_serializer(client_orders, many=True)
        return Response(serializer.data)

class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contarct.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', 'type', 'status', 'duration', 'machine_number', 'description']

    def get_queryset(self):
        queryset = super().get_queryset()
        factory_id = self.request.query_params.get('factory')
        if factory_id:
            queryset = queryset.filter(factory_id=factory_id)
        return queryset

    @action(detail=False, methods=['get'])
    def user_contracts(self, request):
        """
        Get all contracts for the authenticated user.
        """
        contracts = self.queryset.filter(client=request.user)
        page = self.paginate_queryset(contracts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(contracts, many=True)
        return Response(serializer.data)


class ShippingDetialsViewSet(viewsets.ModelViewSet):
    queryset = shipping_detials.objects.all()
    serializer_class = ShippingDetialsSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    search_fields = get_model_search_fields(shipping_detials)

    # action get price depend on from and to
    @action(detail=False, methods=['get'], url_path='get-price')
    def get_price(self, request):
        from_country = request.query_params.get('from')
        to_country = request.query_params.get('to')
        if from_country and to_country:
            shipping = shipping_detials.objects.filter(from_country=from_country, to_country=to_country).first()
            if shipping:
                return Response({'price': shipping.price})
            else:
                return Response({'error': 'Shipping details not found'}, status=404)
        else:
            return Response({'error': 'From and To countries are required'}, status=400)



                

    