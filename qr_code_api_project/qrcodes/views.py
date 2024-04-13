from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.models import User
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import generate_qr_code_image
from django.shortcuts import get_object_or_404
from .models import QRCode
from .serializers import QRCodeSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser


@api_view(['POST'])  # Remove 'GET' from the list of methods
def register(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method "GET" not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            # Generate token
            refresh = RefreshToken.for_user(user)
            return Response({'token': str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        return Response({'message': 'Login endpoint reached'}, status=status.HTTP_200_OK)



@api_view(['POST'])
def generate_qr_code(request):
    type = request.data.get('type')
    data = request.data.get('data')
    
    # Validate the input data (optional)
    if not type or not data:
        return Response({'error': 'Type and data are required.'}, status=status.HTTP_400_BAD_REQUEST)
    
    # Generate the QR code image
    qr_code_image = generate_qr_code_image(data)
    
    # Return the response with the generated QR code details
    return Response({'qr_code_image': qr_code_image}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def get_qr_code_details(request, pk):
    # Retrieve the QR code object by its ID (pk)
    qr_code = get_object_or_404(QRCode, pk=pk)
    
    # Check if the authenticated user owns the QR code (if user-specific)
    # Add your authentication and permission logic here if needed
    
    # Generate the QR code image
    qr_code_image = generate_qr_code_image(qr_code.data)
    
    # Serialize the QR code data if necessary
    # qr_code_serializer = YourQRCodeSerializer(qr_code)
    # serialized_data = qr_code_serializer.data
    
    # Return the response with QR code details and image
    return Response({
        'id': qr_code.id,
        'type': qr_code.type,
        'data': qr_code.data,
        'qr_code_image': qr_code_image
        # Add more fields as needed
    }, status=status.HTTP_200_OK)
    
    
    
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_qr_codes(request):
    # Retrieve all QR codes belonging to the authenticated user
    qr_codes = QRCode.objects.filter(user=request.user)
    
    # Filter QR codes based on type if type is provided in query params
    qr_code_type = request.query_params.get('type')
    if qr_code_type:
        qr_codes = qr_codes.filter(type=qr_code_type)
    
    # Pagination
    paginator = PageNumberPagination()
    paginator.page_size = 10  # Number of items per page
    result_page = paginator.paginate_queryset(qr_codes, request)
    
    # Serialize QR code data
    qr_code_serializer = QRCodeSerializer(result_page, many=True)
    
    # Return paginated QR code data
    return paginator.get_paginated_response(qr_code_serializer.data)  


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_qr_code(request, pk):
    try:
        qr_code = QRCode.objects.get(pk=pk, user=request.user)
    except QRCode.DoesNotExist:
        return Response({"error": "QR code not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = QRCodeSerializer(qr_code, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  
    
    
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_qr_code(request, pk):
    try:
        qr_code = QRCode.objects.get(pk=pk, user=request.user)
    except QRCode.DoesNotExist:
        return Response({"error": "QR code not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        qr_code.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    serializer = UserSerializer(user, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)    