from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .models import service, ServiceRequest
from django.http import JsonResponse
from .serializers import ServiceSerializer, ServiceRequestSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import pusher
from django.conf import settings
from django.db.models import CharField, TextField

# Initialize Pusher
pusher_client = pusher.Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)

# Pagination
class Pagination(PageNumberPagination):
    page_size = 10

class ServicePagination(PageNumberPagination):
    page_size = 10

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = service.objects.all()
    serializer_class = ServiceSerializer
    pagination_class = ServicePagination
    search_fields = [
        field.name
        for field in service._meta.get_fields()
        if isinstance(field, (CharField, TextField))
    ]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        elif self.action in ['list', 'retrieve']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        instance = serializer.save()
        # Trigger Pusher event for new service
        pusher_client.trigger(
            'service-channel',
            'service-created',
            serializer.data
        )

    def perform_update(self, serializer):
        instance = serializer.save()
        # Trigger Pusher event for updated service
        pusher_client.trigger(
            'service-channel',
            'service-updated',
            serializer.data
        )




class ClientRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    @swagger_auto_schema(
        operation_description="Get all requests for the authenticated client",
        responses={200: openapi.Response("Success", ServiceRequestSerializer(many=True))}
    )
    def get(self, request):
        requests = ServiceRequest.objects.filter(client=request.user)
        serializer = ServiceRequestSerializer(requests, many=True)
        return Response({"status_code": 200, "data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new request for the authenticated client",
        request_body=ServiceRequestSerializer,
        responses={201: openapi.Response("Created", ServiceRequestSerializer)}
    )
    def post(self, request):
        data = request.data
        data['client'] = request.user.id
        serializer = ServiceRequestSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status_code": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status_code": 400, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class AdminRequestView(APIView):
    permission_classes = [permissions.IsAdminUser]
    pagination_class = Pagination

    @swagger_auto_schema(
        operation_description="Get all service requests",
        responses={200: openapi.Response("Success", ServiceRequestSerializer(many=True))}
    )
    def get(self, request):
        requests = ServiceRequest.objects.all()
        serializer = ServiceRequestSerializer(requests, many=True)
        return Response({"status_code": 200, "data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new service request",
        request_body=ServiceRequestSerializer,
        responses={201: openapi.Response("Created", ServiceRequestSerializer)}
    )
    def post(self, request):
        serializer = ServiceRequestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status_code": 201, "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status_code": 400, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Update an existing service request",
        request_body=ServiceRequestSerializer,
        responses={200: openapi.Response("Updated", ServiceRequestSerializer)}
    )
    def put(self, request, pk):
        try:
            req = ServiceRequest.objects.get(pk=pk)
        except ServiceRequest.DoesNotExist:
            return Response({"status_code": 404, "error": "Request not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ServiceRequestSerializer(req, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"status_code": 200, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"status_code": 400, "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Delete an existing service request",
        responses={204: openapi.Response("No Content")}
    )
    def delete(self, request, pk):
        try:
            req = ServiceRequest.objects.get(pk=pk)
        except ServiceRequest.DoesNotExist:
            return Response({"status_code": 404, "error": "Request not found"}, status=status.HTTP_404_NOT_FOUND)

        req.delete()
        return Response({"status_code": 204, "data": "Request deleted"}, status=status.HTTP_204_NO_CONTENT)

class TechnicianRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination

    @swagger_auto_schema(
        operation_description="Get all requests assigned to the authenticated technician",
        responses={200: openapi.Response("Success", ServiceRequestSerializer(many=True))}
    )
    def get(self, request):
        requests = ServiceRequest.objects.filter(technician=request.user)
        serializer = ServiceRequestSerializer(requests, many=True)
        return Response({"status_code": 200, "data": serializer.data}, status=status.HTTP_200_OK)