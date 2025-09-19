from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Contact
from .serializers import ContactSerializer, ContactCreateSerializer

# Create your views here.

class HealthCheckView(APIView):
    """
    Health check endpoint to verify the API is running properly.
    Returns basic system information and database connectivity status.
    """
    
    def get(self, request):
        try:
            # Test database connectivity
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"
        
        health_data = {
            "status": "healthy",
            "timestamp": datetime.datetime.now().isoformat(),
            "database": db_status,
            "version": "1.0.0",
            "service": "getcontact-api"
        }
        
        return Response(health_data, status=status.HTTP_200_OK)


class ContactListView(APIView):
    """
    API endpoint to list all contacts and create multiple contacts
    """
    
    @swagger_auto_schema(
        operation_summary="List all contacts",
        operation_description="Retrieve a list of all active contacts with optional filtering by fullname or phone_number",
        manual_parameters=[
            openapi.Parameter(
                'fullname',
                openapi.IN_QUERY,
                description="Filter contacts by fullname (partial match, case-insensitive)",
                type=openapi.TYPE_STRING,
                required=False
            ),
            openapi.Parameter(
                'phone_number',
                openapi.IN_QUERY,
                description="Filter contacts by phone number (partial match, case-insensitive)",
                type=openapi.TYPE_STRING,
                required=False
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successfully retrieved contacts",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, example='success'),
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER, example=5),
                        'filters_applied': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'fullname': openapi.Schema(type=openapi.TYPE_STRING, nullable=True, example='John'),
                                'phone_number': openapi.Schema(type=openapi.TYPE_STRING, nullable=True, example='+123')
                            }
                        ),
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'fullname': openapi.Schema(type=openapi.TYPE_STRING),
                                    'email': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                                    'address': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'country': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'notes': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                                    'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                                }
                            )
                        )
                    }
                )
            )
        }
    )
    def get(self, request):
        """
        Get all contacts with optional filtering by fullname or phone_number
        Query parameters:
        - fullname: Filter contacts by fullname (partial match)
        - phone_number: Filter contacts by phone_number (partial match)
        """
        try:
            # Get all active contacts
            contacts = Contact.objects.filter(is_active=True)
            
            # Apply filters if provided
            fullname_filter = request.query_params.get('fullname', None)
            phone_filter = request.query_params.get('phone_number', None)
            
            if fullname_filter:
                contacts = contacts.filter(fullname__icontains=fullname_filter)
            
            if phone_filter:
                contacts = contacts.filter(phone_number__icontains=phone_filter)
            
            # Serialize the contacts
            serializer = ContactSerializer(contacts, many=True)
            
            return Response({
                'status': 'success',
                'count': contacts.count(),
                'filters_applied': {
                    'fullname': fullname_filter,
                    'phone_number': phone_filter
                },
                'data': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    @swagger_auto_schema(
        operation_summary="Create multiple contacts",
        operation_description="Create multiple contacts from a list of dictionaries. Each dictionary must contain 'fullname' and 'phone_number' fields.",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'fullname': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Contact full name',
                        example='John Doe'
                    ),
                    'phone_number': openapi.Schema(
                        type=openapi.TYPE_STRING,
                        description='Contact phone number',
                        example='+1234567890'
                    )
                },
                required=['fullname', 'phone_number']
            ),
            example=[
                {"fullname": "John Doe", "phone_number": "+1234567890"},
                {"fullname": "Jane Smith", "phone_number": "+0987654321"}
            ]
        ),
        responses={
            201: openapi.Response(
                description="Successfully created contacts",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, example='success'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Successfully created 2 contacts'),
                        'count': openapi.Schema(type=openapi.TYPE_INTEGER, example=2),
                        'data': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'fullname': openapi.Schema(type=openapi.TYPE_STRING),
                                    'email': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
                                    'address': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'country': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'notes': openapi.Schema(type=openapi.TYPE_STRING, nullable=True),
                                    'is_active': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                                    'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_DATETIME),
                                }
                            )
                        )
                    }
                )
            ),
            400: openapi.Response(
                description="Validation error",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, example='error'),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, example='Validation failed'),
                        'errors': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_OBJECT))
                    }
                )
            )
        }
    )
    def post(self, request):
        """
        Create multiple contacts from a list of dictionaries
        Expected request body format:
        [
            {"fullname": "John Doe", "phone_number": "+1234567890"},
            {"fullname": "Jane Smith", "phone_number": "+0987654321"}
        ]
        """
        try:
            # Validate that request data is a list
            if not isinstance(request.data, list):
                return Response({
                    'status': 'error',
                    'message': 'Request body must be a list of dictionaries'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Validate each item in the list
            serializer = ContactCreateSerializer(data=request.data, many=True)
            
            if serializer.is_valid():
                # Create contacts
                contacts = serializer.save()
                
                # Serialize the created contacts for response
                response_serializer = ContactSerializer(contacts, many=True)
                
                return Response({
                    'status': 'success',
                    'message': f'Successfully created {len(contacts)} contacts',
                    'count': len(contacts),
                    'data': response_serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response({
                    'status': 'error',
                    'message': 'Validation failed',
                    'errors': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
