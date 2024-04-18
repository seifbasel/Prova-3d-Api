# serializers.py
from rest_framework import  serializers
from .models import UserProfile, Category, Product, Cart, CartItem, Payment ,Favorite


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id','user','phone_number','address']
        read_only_fields = ['user']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
    

class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'product', 'created_at']  # Adjust fields as needed


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['id', 'cart', 'product']
        
    def validate_quantity(self, value):
        """
        Validate that the quantity does not exceed the available quantity of the product.
        """
        product_id = self.initial_data.get('product')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Invalid product")

        if value > product.quantity:
            raise serializers.ValidationError(f"Quantity exceeds available quantity ({product.quantity})")

        return value


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
