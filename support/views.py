from django.shortcuts import render
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .models import supportTicket
from django.http import JsonResponse
from .serializers import SupportTicketSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.

class Pagination(PageNumberPagination):
    page_size = 10

from django.db.models import CharField, TextField


class SupportTicketViewSet(viewsets.ModelViewSet):
    queryset = supportTicket.objects.all()
    serializer_class = SupportTicketSerializer
    pagination_class = Pagination
    search_fields = [
        field.name
        for field in supportTicket._meta.get_fields()
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


    @swagger_auto_schema(
        operation_description="Create a new support ticket",
        request_body=SupportTicketSerializer,
        responses={
            201: SupportTicketSerializer,
            400: "Bad Request",
            401: "Unauthorized",
            403: "Forbidden"
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @swagger_auto_schema(
        operation_description="Retrieve a support ticket by ID",
        responses={
            200: SupportTicketSerializer,
            404: "Not Found",
            401: "Unauthorized",
            403: "Forbidden"
        }
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
        



            
