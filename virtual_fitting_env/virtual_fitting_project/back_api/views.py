# views.py
from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from django.forms import ValidationError
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserProfile, Category, Product, Cart, CartItem ,Favorite,Order
from .serializers import (SignupSerializer, UserProfileSerializer, CategorySerializer,
                           ProductSerializer,FavoriteSerializer,
                           CartSerializer, CartItemSerializer,OrderSerializer
                            )
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from back_api.permission import IsAdminOrReadOnly 
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from back_api.serializers import LogoutSerializer,AddToCartSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from django.db import transaction


# In views.py
from django.http import HttpResponse

def index(request):
    return HttpResponse("Welcome to our virtual fitting API!")

# class SignupViewSet(viewsets.ViewSet):
#     """
#     View set to handle user signup.
#     """
#     @action(detail=False, methods=['post'], permission_classes=[AllowAny])
#     def signup(self, request):
#         """
#         Create a new user and generate a JWT token.

#         Parameters:
#         - username: The username of the new user.
#         - email: The email of the new user.
#         - password: The password of the new user.

#         Returns:
#         - A response indicating success or failure of the signup process.
#         """
#         User = get_user_model()
#         username = request.data.get('username')
#         email = request.data.get('email')
#         password = request.data.get('password')
#         phone_number = request.data.get('phone_number')
#         address = request.data.get('address')
#         image = request.data.get('image')

#         if not all([username, email, password]):
#             return Response({'error': 'Username, email, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.create_user(username=username, email=email, password=password)
#             UserProfile.objects.create(user=user, phone_number=phone_number, image=image, address=address)

#             # Generate a JWT token
#             refresh = RefreshToken.for_user(user)
#             return Response({'message': 'User registered successfully', 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
#         except IntegrityError:
#             return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)

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
                phone_number = serializer.validated_data.get('phone_number')
                address = serializer.validated_data.get('address')
                image = serializer.validated_data.get('image')

                UserProfile.objects.create(user=user, phone_number=phone_number, image=image, address=address)

                # Generate a JWT token
                refresh = RefreshToken.for_user(user)
                return Response({'message': 'User registered successfully', 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class SignupViewSet(viewsets.ViewSet):
#     """
#     View set to handle user signup.
#     """
#     @action(detail=False, methods=['post'], permission_classes=[AllowAny])
#     def signup(self, request):
#         """
#         Create a new user and generate a JWT token.

#         Parameters:
#         - username: The username of the new user.
#         - email: The email of the new user.
#         - password: The password of the new user.
#         - phone_number: The phone number of the new user.
#         - address: The address of the new user.
#         - image: The image of the new user.

#         Returns:
#         - A response indicating success or failure of the signup process.
#         """
#         serializer = SignupSerializer(data=request.data)
#         if serializer.is_valid():
#             username = serializer.validated_data.get('username')
#             email = serializer.validated_data.get('email')
#             password = serializer.validated_data.get('password')
#             phone_number = serializer.validated_data.get('phone_number')
#             address = serializer.validated_data.get('address')
#             image = serializer.validated_data.get('image')

#             try:
#                 User = get_user_model()
#                 user = User.objects.create_user(username=username, email=email, password=password)
#                 UserProfile.objects.create(user=user, phone_number=phone_number, image=image, address=address)

#                 # Generate a JWT token
#                 refresh = RefreshToken.for_user(user)
#                 return Response({'message': 'User registered successfully', 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
#             except IntegrityError:
#                 return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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

        if not all([username, password]):
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



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


    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        category_name = self.request.query_params.get('category')
        brand_name=self.request.query_params.get('brand')
        color_name = self.request.query_params.get('color')
        size = self.request.query_params.get('size')
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
        
        return queryset


class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint to retrieve, update, or delete a product by ID.

    GET: Retrieve a product by ID.
    PUT: Update a product by ID.
    PATCH: Partially update a product by ID.
    DELETE: Delete a product by ID.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]  # Restrict access to authenticated users only


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


class FavoriteRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint to retrieve, update, or delete a favorite product by ID.

    GET: Retrieve a favorite product by ID.
    PUT: Update a favorite product by ID.
    PATCH: Partially update a favorite product by ID.
    DELETE: Delete a favorite product by ID.
    """
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only allow the authenticated user to access their own favorites
        return Favorite.objects.filter(user=self.request.user)


# Cart Endpoints

# class CartItemListCreateAPIView(generics.ListCreateAPIView):
#     """
#     Endpoint to list all cart items or create a new cart item.

#     GET: Retrieve a list of all cart items.
#     POST: Create a new cart item.
#     """
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer
#     permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only

#     def get_queryset(self):
#         # Get the user's cart items
#         user_profile = get_object_or_404(UserProfile, user=self.request.user)
#         return CartItem.objects.filter(cart__user=user_profile)

#     def post(self, request, *args, **kwargs):
#         serializer = AddToCartSerializer(data=request.data)
#         if serializer.is_valid():
#             product_id = serializer.validated_data['product_id']
#             product = get_object_or_404(Product, pk=product_id)

#             # Check if the product quantity is greater than 0
#             if product.quantity <= 0:
#                 return Response({'error': 'Product is out of stock'}, status=status.HTTP_400_BAD_REQUEST)

#             # Get the UserProfile associated with the User
#             user_profile = UserProfile.objects.get(user=request.user)

#             # Get or create the user's cart
#             cart, created = Cart.objects.get_or_create(user=user_profile)

#             # Check if the product is already in the cart
#             try:
#                 cart_item = CartItem.objects.get(cart=cart, product=product)
#                 # Check if adding one more quantity would exceed the available quantity
#                 if cart_item.quantity + 1 > product.quantity:
#                     return Response({'error': 'Quantity exceeds available stock'}, status=status.HTTP_400_BAD_REQUEST)
#                 # If the product already exists in the cart and adding one more quantity is okay,
#                 # increment the quantity by one
#                 cart_item.quantity += 1
#                 cart_item.save()
#             except CartItem.DoesNotExist:
#                 # If the product is not in the cart, create a new cart item
#                 cart_item = CartItem.objects.create(cart=cart, product=product)

#             return Response({'success': 'Product added to cart'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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


# class CartItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     """
#     Endpoint to retrieve, update, or delete a cart item by ID.

#     GET: Retrieve a cart item by ID.
#     PUT: Update a cart item by ID.
#     PATCH: Partially update a cart item by ID.
#     DELETE: Delete a cart item by ID.
#     """
#     queryset = CartItem.objects.all()
#     serializer_class = CartItemSerializer
#     permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only

#     def get_queryset(self):
#         # Get the UserProfile instance associated with the current user
#         user_profile = get_object_or_404(UserProfile, user=self.request.user)
#         # Filter cart items based on the current user's cart
#         return CartItem.objects.filter(cart__user=user_profile)
    


class CartItemRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint to retrieve, update, or delete a cart item by ID.

    GET: Retrieve a cart item by ID.
    PUT: Update a cart item by ID.
    PATCH: Partially update a cart item by ID.
    DELETE: Delete a cart item by ID.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only

    def get_queryset(self):
        # Get the UserProfile instance associated with the current user
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        # Filter cart items based on the current user's cart
        return CartItem.objects.filter(cart__user=user_profile)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {'message': 'Cart item deleted successfully'},
            status=status.HTTP_204_NO_CONTENT
        )

    def perform_destroy(self, instance):
        instance.delete()

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