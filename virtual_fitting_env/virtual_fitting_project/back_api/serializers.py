# serializers.py
from rest_framework import  serializers
from .models import UserProfile, Category, Product, Cart, CartItem ,Favorite,Order
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.core.exceptions import ValidationError
from rest_framework.response import Response



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','user','phone_number','image','address']
        read_only_fields = ['user']


# class SignupSerializer(serializers.Serializer):
#     username = serializers.CharField(max_length=150)
#     email = serializers.EmailField()
#     password = serializers.CharField(max_length=128)
#     password_confirm = serializers.CharField(max_length=128)
#     phone_number = serializers.CharField(max_length=15, required=False)
#     address = serializers.CharField(max_length=100, required=False)
#     image = serializers.ImageField(required=False)

#     def validate(self, data):
#         password = data.get('password')
#         password_confirm = data.get('password_confirm')

#         if password != password_confirm:
#             raise ValidationError({"error": "Passwords do not match"})

#         try:
#             validate_password(password)
#         except ValidationError as e:
#             error_messages = {"error": []}
#             for message in e.messages:
#                 error_messages["error"].append(message)
#             raise ValidationError(error_messages)

#         return data

#     def create(self, validated_data):
#         validated_data.pop('password_confirm')  # Remove password_confirm from the data
#         user_data = {
#             'username': validated_data['username'],
#             'email': validated_data['email'],
#             'password': validated_data['password'],
#         }
#         user = get_user_model().objects.create_user(**user_data)
#         return user


class SignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
    password_confirm = serializers.CharField(max_length=128)
    phone_number = serializers.CharField(max_length=15, required=False)
    address = serializers.CharField(max_length=100, required=False)
    image = serializers.ImageField(required=False)

    def validate(self, data):
        password = data.get('password')
        password_confirm = data.get('password_confirm')

        # Validate password match
        if password != password_confirm:
            raise ValidationError({"error": ["Passwords do not match"]})

        # Validate password strength
        try:
            validate_password(password)
        except ValidationError as e:
            raise ValidationError({"error": e.messages})

        return data

    def create(self, validated_data):
        validated_data.pop('password_confirm')  # Remove password_confirm from the data
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
            'password': validated_data['password'],
        }
        user = get_user_model().objects.create_user(**user_data)
        return user

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)
    

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    

class FavoriteSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Favorite
        fields = ['product', 'created_at']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']

        # Check if the favorite already exists for the user and product
        if Favorite.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("Product already exists in favorites.")

        # Create the new favorite
        validated_data['user'] = user
        return super().create(validated_data)


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

    def validate(self, data):
        product_id = data.get('product_id')
        if not Product.objects.filter(pk=product_id, quantity__gt=0).exists():
            raise serializers.ValidationError("Product is out of stock.")
        return data


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'