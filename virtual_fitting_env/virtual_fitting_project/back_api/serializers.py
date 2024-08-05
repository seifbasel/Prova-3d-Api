# serializers.py
from rest_framework import  serializers
from .models import  UserProfile, Category, Product, Cart, CartItem ,Favorite,Order,Comment,review
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.core.exceptions import ValidationError


class UserProfileSerializer(serializers.ModelSerializer):
    user_name = serializers.ReadOnlyField(source='user.username')
    user_email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'user_name', 'user_email', 'phone_number', 'image', 'address']
        read_only_fields = ['user']


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
            raise ValidationError({"error": "Passwords do not match"})

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


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    author_image = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id','user','text','sentiment','author_image','created_at']
        read_only_fields = ['product', 'user', 'sentiment', 'author_image']

    def get_author_image(self, obj):
        request = self.context.get('request')
        if obj.user.userprofile and obj.user.userprofile.image:
            return request.build_absolute_uri(obj.user.userprofile.image.url) if request else None
        return None
    

class ProductSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        
        # Handle CharField for image URLs
        image_url = instance.image
        if image_url and not image_url.startswith('http'):
            image_url = self.context['request'].build_absolute_uri(image_url)

        representation['image'] = image_url
        return representation


class FavoriteSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = Favorite
        fields = ['id', 'product']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        product = validated_data['product']

        # Check if the favorite already exists for the user and product
        if Favorite.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError({"error": "Product already exists in favorites."})

        # Create the new favorite
        validated_data['user'] = user
        return super().create(validated_data)
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        product_representation = ProductSerializer(instance.product, context=self.context).data
        
        # Handle CharField for image URLs
        image_url = instance.product.image
        if image_url and not image_url.startswith('http'):
            image_url = self.context['request'].build_absolute_uri(image_url)

        product_representation['image'] = image_url
        representation['product'] = product_representation
        return representation


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = '__all__'

class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']  # Adjust fields as per your needs
        
    def get_total_price(self, obj):
        total_price = 0
        for item in obj.items.all():
            total_price += item.product.price * item.quantity
        return total_price
        

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = review
        fields = '__all__'