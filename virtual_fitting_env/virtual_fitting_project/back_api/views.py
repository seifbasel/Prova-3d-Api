# views.py
from django.contrib.auth import authenticate
from django.db import IntegrityError
from django.http import HttpResponse
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserProfile, Category, Product, Cart, CartItem ,Favorite,Order, review
from .serializers import (ReviewSerializer, SignupSerializer, UserProfileSerializer, CategorySerializer,
                           ProductSerializer,FavoriteSerializer,
                           CartSerializer, CartItemSerializer,OrderSerializer
                            )
from rest_framework.permissions import IsAuthenticated, AllowAny
from back_api.permission import IsAdminOrReadOnly 
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from back_api.serializers import LogoutSerializer,AddToCartSerializer
from rest_framework.views import APIView
from django.db import transaction
from rest_framework import generics
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

def ping(request):
    return HttpResponse("pong")

class SignupViewSet(viewsets.ViewSet):
    """
    View set to handle user signup.
    """
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
        """
        Create a new user and generate a JWT token.

        Parameters:
        - username: The username of the new user.
        - email: The email of the new user.
        - password: The password of the new user.
        - password_confirm: The password confirmation.
        - phone_number: The phone number of the new user.
        - address: The address of the new user.
        - image: The image of the new user.

        Returns:
        - A response indicating success or failure of the signup process.
        """
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
                # Additional user profile data
                phone_number = serializer.validated_data.get('phone_number','')
                address = serializer.validated_data.get('address', '')  # Default to empty string if not provided
                image = serializer.validated_data.get('image', None)
                UserProfile.objects.create(user=user, phone_number=phone_number, address=address, image=image)
                # Generate a JWT token
                refresh = RefreshToken.for_user(user)
                return Response({'message': 'User registered successfully', 'access': str(refresh.access_token),'refresh': str(refresh)}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': serializer.errors.get('error', 'Invalid data')}, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ViewSet):
    """
    View set to handle user login.
    """
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Authenticate a user and generate JWT tokens.

        Parameters:
        - username: The username of the user.
        - password: The password of the user.

        Returns:
        - A response containing JWT access and refresh tokens if authentication succeeds,
          or an error message if authentication fails.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class LogoutViewSet(viewsets.ViewSet):
    """
    View set to handle user logout.
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['post'])
    def logout(self, request):
        """
        Invalidate the user's JWT tokens upon logout.

        Returns:
        - A response indicating successful logout.
        """
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data.get('refresh_token')
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': 'Invalid refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# user profile end point

class UserProfileRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    Endpoint to retrieve and update user profile information.
    
    GET: Retrieve the current user's profile.
    PUT/PATCH: Update the current user's profile.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # Retrieve the profile of the current authenticated user
        return self.request.user.userprofile

    def perform_update(self, serializer):
        # Ensure that the user field remains unchanged during update
        serializer.save(user=self.request.user)


# Category Endpoints

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all categories or create a new category.

    GET: Retrieve a list of all categories.
    POST: Create a new category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


# Product Endpoints

class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all products or create a new product.

    GET: Retrieve a list of all products or products filtered by name.
    POST: Create a new product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]  # Restrict access to authenticated users only

    #searching
    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        category_name = self.request.query_params.get('category')
        brand_name=self.request.query_params.get('brand')
        color_name = self.request.query_params.get('color')
        size = self.request.query_params.get('size')
        gender = self.request.query_params.get('gender')

        if name:
            queryset = queryset.filter(name__icontains=name)
        if category_name:
            queryset = queryset.filter(category__name=category_name)
        if brand_name:
            queryset = queryset.filter(brand__name=brand_name)
        if color_name:
            queryset = queryset.filter(color__icontains=color_name)
        if size:
            queryset = queryset.filter(size__icontains=size)
        if gender:
            queryset = queryset.filter(gender=gender)
        return queryset


# Favorite Endpoints

class FavoriteListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all favorite products or create a new favorite product.

    GET: Retrieve a list of all favorite products.
    POST: Create a new favorite product.
    """
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return favorites of the authenticated user
        return Favorite.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically set the user to the authenticated user
        serializer.save(user=self.request.user)


class FavoriteDeleteAPIView(generics.DestroyAPIView):
    """
    Endpoint to delete a favorite product using product ID in the request body.

    DELETE: Delete a favorite product by product ID.
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the favorite item for the authenticated user and the specified product
        favorite = get_object_or_404(Favorite, user=request.user, product_id=product_id)

        # Delete the favorite item
        favorite.delete()
        return Response({'message': 'Favorite deleted successfully'},status=status.HTTP_204_NO_CONTENT)
    


# Cart Endpoints
class CartItemListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all cart items or create a new cart item.

    GET: Retrieve a list of all cart items.
    POST: Create a new cart item.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only

    def get_queryset(self):
        # Get the user's cart items
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        return CartItem.objects.filter(cart__user=user_profile)

    def post(self, request, *args, **kwargs):
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            product_id = serializer.validated_data['product_id']
            product = get_object_or_404(Product, pk=product_id)

            # Check if the product quantity is greater than 0
            if product.quantity <= 0:
                return Response({'error': 'Product is out of stock'}, status=status.HTTP_400_BAD_REQUEST)

            # Get the UserProfile associated with the User
            user_profile = UserProfile.objects.get(user=request.user)

            # Get or create the user's cart
            cart, created = Cart.objects.get_or_create(user=user_profile)

            # Check if the product is already in the cart
            try:
                cart_item = CartItem.objects.get(cart=cart, product=product)
                # Check if adding one more quantity would exceed the available quantity
                if cart_item.quantity + 1 > product.quantity:
                    return Response({'error': 'Quantity exceeds available stock'}, status=status.HTTP_400_BAD_REQUEST)
                # If the product already exists in the cart and adding one more quantity is okay,
                # increment the quantity by one
                cart_item.quantity += 1
                cart_item.save()
            except CartItem.DoesNotExist:
                # If the product is not in the cart, create a new cart item
                cart_item = CartItem.objects.create(cart=cart, product=product)

            return Response(CartItemSerializer(cart_item).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartItemDeleteAPIView(generics.DestroyAPIView):
    """
    Endpoint to delete a cart item using product ID in the request body.

    DELETE: Delete a cart item by product ID.
    """
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only

    def delete(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        user_profile = get_object_or_404(UserProfile, user=request.user)
        cart = get_object_or_404(Cart, user=user_profile)
        cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)

        cart_item.delete()
        return Response({'message': 'Cart item deleted successfully'},status=status.HTTP_204_NO_CONTENT)


class CartTotalAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_profile = UserProfile.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart__user=user_profile)

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        return Response({'total_price': total_price}, status=200)

# CheckoutEndpoint 

class CheckoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_profile = request.user.userprofile
        cart_items = CartItem.objects.filter(cart__user=user_profile)
        
        # Check if the cart is empty
        if not cart_items:
            return Response({'message': 'Cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        # Begin transaction to ensure atomicity
        with transaction.atomic():
            # Create an order
            order = Order.objects.create(
                user=user_profile,
                total_price=total_price,
                status='Pending',  # You can change this based on your workflow
                shipping_address=request.data.get('shipping_address')  # Assuming shipping address is provided in request data
            )

            # Initialize an empty list to store product data
            products_data = []

            # Remove purchased items from the database and update product quantity
            for cart_item in cart_items:
                product = cart_item.product
                
                # Check if the product quantity is sufficient for the cart item
                if product.quantity < cart_item.quantity:
                    return Response({'message': f'Insufficient quantity for product {product.name}'}, status=status.HTTP_400_BAD_REQUEST)
                
                # Reduce the product quantity
                product.quantity -= cart_item.quantity
                product.save()
                
                # Serialize the product associated with the cart item
                product_serializer = ProductSerializer(product)
                product_data = product_serializer.data
                
                # Include the quantity of the purchased product in the product data
                product_data['quantity'] = cart_item.quantity
                
                # Add the product data to the list of products related to the order
                products_data.append(product_data)
                
                # Delete the cart item
                cart_item.delete()

        # Serialize the order
        order_serializer = OrderSerializer(order)
        order_data = order_serializer.data
        
        # Assign the list of products to the order data
        order_data['products'] = products_data

        return Response({'message': 'Checkout successful', 'order': order_data}, status=status.HTTP_201_CREATED)
    

#  comments end point

from .sentement import predict_sentiment

class CommentListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all comments for a product or create a new comment.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Comment.objects.filter(product_id=product_id)

    def perform_create(self, serializer):
        product_id = self.kwargs['product_id']
        product = generics.get_object_or_404(Product, pk=product_id)
        text = serializer.validated_data.get('text')
        
        # Predict the sentiment of the comment
        sentiment = predict_sentiment(text)
        
        serializer.save(product=product, user=self.request.user, sentiment=sentiment)  # Save with sentiment


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint to retrieve, update, or delete a comment by ID.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)
    
    
# reviews end point
class ReviewListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all reviews or create a new review.
    """
    queryset = review.objects.all()
    serializer_class = ReviewSerializer
    
    def perform_create(self, serializer):
        text = serializer.validated_data.get('text')
        
        # Implement your sentiment analysis logic here
        sentiment = predict_sentiment(text)
        
        serializer.save(sentiment=sentiment)