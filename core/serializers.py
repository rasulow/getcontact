from rest_framework import serializers
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    """
    Serializer for Contact model
    """
    
    class Meta:
        model = Contact
        fields = [
            'id',
            'fullname',
            'email',
            'phone_number',
            'address',
            'country',
            'notes',
            'is_active',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ContactCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating contacts with minimal required fields
    """
    
    class Meta:
        model = Contact
        fields = ['fullname', 'phone_number']
    
    def validate_fullname(self, value):
        """Validate fullname field"""
        if not value or not value.strip():
            raise serializers.ValidationError("Fullname cannot be empty")
        return value.strip()
    
    def validate_phone_number(self, value):
        """Validate phone_number field"""
        if not value or not value.strip():
            raise serializers.ValidationError("Phone number cannot be empty")
        return value.strip()
