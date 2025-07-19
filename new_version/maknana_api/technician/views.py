from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from machine_and_factory.models import malfunction_report, malfunction_request, malfunction_invoice
from service.models import request_report, ServiceRequest, request_invoice
from .serializers import MalfunctionReportSerializer, MalfunctionRequestSerializer, MalfunctionInvoiceSerializer, RequestReportSerializer, ServiceRequestSerializer, RequestInvoiceSerializer
from core.models import CustomUser

class TechnicianReportsAPIView(APIView):
    def get(self, request, technician_id, format=None):
        try:
            technician = CustomUser.objects.get(id=technician_id, type='technician')
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Technician not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Optimize queries with select_related and prefetch_related
        malfunction_reports = malfunction_report.objects.filter(
            malfunction_request__technician=technician
        ).select_related('malfunction_request', 'malfunction_request__technician')
        service_reports = request_report.objects.filter(
            technician=technician
        ).select_related('technician', 'service_request')  # Adjust 'request' if field name differs

        malfunction_serializer = MalfunctionReportSerializer(malfunction_reports, many=True)
        service_serializer = RequestReportSerializer(service_reports, many=True)

        return Response({
            'malfunction_reports': malfunction_serializer.data,
            'service_reports': service_serializer.data
        }, status=status.HTTP_200_OK)

class TechnicianTasksAPIView(APIView):
    def get(self, request, technician_id, format=None):
        try:
            technician = CustomUser.objects.get(id=technician_id, type='technician')
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Technician not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Optimize queries with select_related
        malfunction_requests = malfunction_request.objects.filter(
            technician=technician
        ).select_related('technician', 'client', 'machine', 'type')
        service_requests = ServiceRequest.objects.filter(
            technician=technician
        ).select_related('technician', 'client', 'service')  # Adjust 'service' if named differently

        malfunction_serializer = MalfunctionRequestSerializer(malfunction_requests, many=True)
        service_serializer = ServiceRequestSerializer(service_requests, many=True)

        return Response({
            'malfunction_tasks': malfunction_serializer.data,
            'service_tasks': service_serializer.data
        }, status=status.HTTP_200_OK)

class TechnicianInvoicesAPIView(APIView):
    def get(self, request, technician_id, format=None):
        try:
            technician = CustomUser.objects.get(id=technician_id, type='technician')
        except CustomUser.DoesNotExist:
            return Response({'detail': 'Technician not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Optimize queries
        malfunction_invoices = malfunction_invoice.objects.filter(
            malfunction_request__technician=technician
        ).select_related('malfunction_request', 'malfunction_request__technician')
        service_invoices = request_invoice.objects.filter(
            technician=technician
        ).select_related('technician', 'service_request')  # Adjust 'request' if field name differs

        malfunction_serializer = MalfunctionInvoiceSerializer(malfunction_invoices, many=True)
        service_serializer = RequestInvoiceSerializer(service_invoices, many=True)

        return Response({
            'malfunction_invoices': malfunction_serializer.data,
            'service_invoices': service_serializer.data
        }, status=status.HTTP_200_OK)










# from django.shortcuts import render
# # Create your views here.

# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from machine_and_factory.models import malfunction_report, malfunction_request, malfunction_invoice
# from service.models import request_report, ServiceRequest, request_invoice
# from .serializers import MalfunctionReportSerializer, MalfunctionRequestSerializer, MalfunctionInvoiceSerializer, RequestReportSerializer, ServiceRequestSerializer, RequestInvoiceSerializer
# from core.models import CustomUser

# class TechnicianReportsAPIView(APIView):
#     def get(self, request, technician_id, format=None):
#         try:
#             technician = CustomUser.objects.get(id=technician_id, type='technician')
#         except CustomUser.DoesNotExist:
#             return Response({'detail': 'Technician not found.'}, status=status.HTTP_404_NOT_FOUND)

#         malfunction_reports = malfunction_report.objects.filter(malfunction_request__technician=technician)
#         service_reports = request_report.objects.filter(technician=technician)

#         malfunction_serializer = MalfunctionReportSerializer(malfunction_reports, many=True)
#         service_serializer = RequestReportSerializer(service_reports, many=True)

#         return Response({
#             'malfunction_reports': malfunction_serializer.data,
#             'service_reports': service_serializer.data
#         }, status=status.HTTP_200_OK)

# class TechnicianTasksAPIView(APIView):
#     def get(self, request, technician_id, format=None):
#         try:
#             technician = CustomUser.objects.get(id=technician_id, type='technician')
#         except CustomUser.DoesNotExist:
#             return Response({'detail': 'Technician not found.'}, status=status.HTTP_404_NOT_FOUND)

#         malfunction_requests = malfunction_request.objects.filter(technician=technician)
#         service_requests = ServiceRequest.objects.filter(technician=technician)

#         malfunction_serializer = MalfunctionRequestSerializer(malfunction_requests, many=True)
#         service_serializer = ServiceRequestSerializer(service_requests, many=True)

#         return Response({
#             'malfunction_tasks': malfunction_serializer.data,
#             'service_tasks': service_serializer.data
#         }, status=status.HTTP_200_OK)

# class TechnicianInvoicesAPIView(APIView):
#     def get(self, request, technician_id, format=None):
#         try:
#             technician = CustomUser.objects.get(id=technician_id, type='technician')
#         except CustomUser.DoesNotExist:
#             return Response({'detail': 'Technician not found.'}, status=status.HTTP_404_NOT_FOUND)

#         malfunction_invoices = malfunction_invoice.objects.filter(malfunction_request__technician=technician)
#         service_invoices = request_invoice.objects.filter(technician=technician)

#         malfunction_serializer = MalfunctionInvoiceSerializer(malfunction_invoices, many=True)
#         service_serializer = RequestInvoiceSerializer(service_invoices, many=True)

#         return Response({
#             'malfunction_invoices': malfunction_serializer.data,
#             'service_invoices': service_serializer.data
#         }, status=status.HTTP_200_OK)


