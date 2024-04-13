# serializers.py
from rest_framework import serializers
from .models import CustomUser, Category, Product, Cart, CartItem, Payment
from rest_framework import  serializers, viewsets
from .models import CustomUser


MIN_LENGTH = 8

from rest_framework import serializers
from .models import CustomUser

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        min_length=8,
        error_messages={"min_length": "Password must be at least 8 characters long."}
    )

    class Meta:
        model = CustomUser
        fields = ["username", "email", "password", "first_name", "last_name", "phone_number", "address", "gender"]
        extra_kwargs = {
            'password': {'write_only': True},
            'groups': {'read_only': True},
            'user_permissions': {'read_only': True}
        }

    def validate(self, data):
        # Check if password and password2 match
        if 'password' in data and 'password2' in data and data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        # Remove password2 from validated_data
        validated_data.pop('password2', None)
        # Create user without password2
        user = CustomUser.objects.create_user(**validated_data)
        return user



# class CustomUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
