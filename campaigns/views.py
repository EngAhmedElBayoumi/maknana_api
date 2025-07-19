from django.shortcuts import render
from .models import Campaign
from .serializers import CampaignSerializer
from rest_framework import viewsets, permissions, filters
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from rest_framework.views import APIView

# Create your views here.

class Pagination(PageNumberPagination):
    page_size = 10


class CampaignViewSet(viewsets.ModelViewSet):
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = Pagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'target_audience', 'description']
    

