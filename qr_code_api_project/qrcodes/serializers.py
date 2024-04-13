from rest_framework import serializers
from django.contrib.auth.models import User
from .models import QRCode, Tag

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined', 'is_staff', 'is_active']
        
class TagSerializer(serializers.ModelSerializer):
    """
    Serializer for the Tag model.
    """
    class Meta:
        model = Tag
        fields = ['id', 'name']
        
                
class QRCodeSerializer(serializers.ModelSerializer):
    """
    Serializer for the QRCode model.
    """
    tags = TagSerializer(many=True, read_only=True)
    class Meta:
        model = QRCode
        fields = ['id', 'user', 'type', 'data', 'created_at', 'is_public', 'tags']        