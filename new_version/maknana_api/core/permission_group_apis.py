from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from .models import CustomUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename', 'content_type']

class UserPermissionGroupSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True, read_only=True)
    permissions = PermissionSerializer(many=True, read_only=True, source='user_permissions')

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'name', 'groups', 'permissions']

class AssignGroupSerializer(serializers.Serializer):
    group_ids = serializers.ListField(child=serializers.IntegerField(), required=True)

class AssignPermissionSerializer(serializers.Serializer):
    permission_ids = serializers.ListField(child=serializers.IntegerField(), required=True)

class PermissionGroupViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(
        operation_description="List all groups",
        responses={
            200: GroupSerializer(many=True)
        }
    )
    @action(detail=False, methods=['get'], url_path='groups')
    def list_groups(self, request):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response({"status_code": 200, "data": serializer.data}, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Create a new group",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="Group name"),
                'permission_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description="List of permission IDs")
            },
            required=['name']
        ),
        responses={
            201: GroupSerializer,
            400: "Invalid data provided"
        }
    )
    @action(detail=False, methods=['post'], url_path='groups/create')
    def create_group(self, request):
        name = request.data.get('name')
        permission_ids = request.data.get('permission_ids', [])
        
        if not name:
            return Response({
                "status_code": 400,
                "error": "Group name is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        group = Group.objects.create(name=name)
        if permission_ids:
            permissions = Permission.objects.filter(id__in=permission_ids)
            group.permissions.set(permissions)
        
        serializer = GroupSerializer(group)
        return Response({
            "status_code": 201,
            "data": serializer.data
        }, status=status.HTTP_201_CREATED)

    @swagger_auto_schema(
        operation_description="Update a group",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'name': openapi.Schema(type=openapi.TYPE_STRING, description="Group name"),
                'permission_ids': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_INTEGER), description="List of permission IDs")
            }
        ),
        responses={
            200: GroupSerializer,
            404: "Group not found",
            400: "Invalid data provided"
        }
    )
    @action(detail=True, methods=['put'], url_path='groups/update')
    def update_group(self, request, pk=None):
        try:
            group = Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            return Response({
                "status_code": 404,
                "error": "Group not found"
            }, status=status.HTTP_404_NOT_FOUND)

        name = request.data.get('name')
        permission_ids = request.data.get('permission_ids', [])

        if name:
            group.name = name
        if permission_ids:
            permissions = Permission.objects.filter(id__in=permission_ids)
            group.permissions.set(permissions)
        
        group.save()
        serializer = GroupSerializer(group)
        return Response({
            "status_code": 200,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Delete a group",
        responses={
            204: "Group deleted successfully",
            404: "Group not found"
        }
    )
    @action(detail=True, methods=['delete'], url_path='groups/delete')
    def delete_group(self, request, pk=None):
        try:
            group = Group.objects.get(pk=pk)
            group.delete()
            return Response({
                "status_code": 204,
                "data": "Group deleted successfully"
            }, status=status.HTTP_204_NO_CONTENT)
        except Group.DoesNotExist:
            return Response({
                "status_code": 404,
                "error": "Group not found"
            }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="List all permissions",
        responses={
            200: PermissionSerializer(many=True)
        }
    )
    @action(detail=False, methods=['get'], url_path='permissions')
    def list_permissions(self, request):
        permissions = Permission.objects.all()
        serializer = PermissionSerializer(permissions, many=True)
        return Response({
            "status_code": 200,
            "data": serializer.data
        }, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Get user permissions and groups",
        responses={
            200: UserPermissionGroupSerializer,
            404: "User not found"
        }
    )
    @action(detail=True, methods=['get'], url_path='user/(?P<user_id>[^/.]+)/permissions')
    def get_user_permissions(self, request, user_id=None):
        try:
            user = CustomUser.objects.get(id=user_id)
            serializer = UserPermissionGroupSerializer(user)
            return Response({
                "status_code": 200,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({
                "status_code": 404,
                "error": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Assign groups to a user",
        request_body=AssignGroupSerializer,
        responses={
            200: UserPermissionGroupSerializer,
            404: "User not found",
            400: "Invalid group IDs"
        }
    )
    @action(detail=True, methods=['post'], url_path='user/(?P<user_id>[^/.]+)/assign-groups')
    def assign_groups(self, request, user_id=None):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({
                "status_code": 404,
                "error": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AssignGroupSerializer(data=request.data)
        if serializer.is_valid():
            group_ids = serializer.validated_data['group_ids']
            groups = Group.objects.filter(id__in=group_ids)
            if len(groups) != len(group_ids):
                return Response({
                    "status_code": 400,
                    "error": "One or more group IDs are invalid"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.groups.set(groups)
            user_serializer = UserPermissionGroupSerializer(user)
            return Response({
                "status_code": 200,
                "data": user_serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status_code": 400,
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_description="Assign permissions to a user",
        request_body=AssignPermissionSerializer,
        responses={
            200: UserPermissionGroupSerializer,
            404: "User not found",
            400: "Invalid permission IDs"
        }
    )
    @action(detail=True, methods=['post'], url_path='user/(?P<user_id>[^/.]+)/assign-permissions')
    def assign_permissions(self, request, user_id=None):
        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response({
                "status_code": 404,
                "error": "User not found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = AssignPermissionSerializer(data=request.data)
        if serializer.is_valid():
            permission_ids = serializer.validated_data['permission_ids']
            permissions = Permission.objects.filter(id__in=permission_ids)
            if len(permissions) != len(permission_ids):
                return Response({
                    "status_code": 400,
                    "error": "One or more permission IDs are invalid"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user.user_permissions.set(permissions)
            user_serializer = UserPermissionGroupSerializer(user)
            return Response({
                "status_code": 200,
                "data": user_serializer.data
            }, status=status.HTTP_200_OK)
        return Response({
            "status_code": 400,
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)