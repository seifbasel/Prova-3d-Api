# views.py
from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import UserProfile, Category, Product, Cart, CartItem, Payment
from .serializers import UserProfileSerializer, CategorySerializer, ProductSerializer, CartSerializer, CartItemSerializer, PaymentSerializer
from django.contrib.auth import get_user_model
from .serializers import UserProfileSerializer


class SignupViewSet(viewsets.ViewSet):
    """
    View set to handle user signup.
    """
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def signup(self, request):
        """
        Create a new user and generate a token.

        Parameters:
        - username: The username of the new user.
        - email: The email of the new user.
        - password: The password of the new user.

        Returns:
        - A response indicating success or failure of the signup process.
        """
        User = get_user_model()
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if not all([username, email, password]):
            return Response({'error': 'Username, email, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            token, _ = Token.objects.get_or_create(user=user)  # Generate token
            return Response({'message': 'User registered successfully', 'token': token.key}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ViewSet):
    """
    View set to handle user login.
    """
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Authenticate a user and generate an authentication token.

        Parameters:
        - username: The username of the user.
        - password: The password of the user.

        Returns:
        - A response containing an authentication token if authentication succeeds, or an error message if authentication fails.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not all([username, password]):
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



class UserListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all users or create a new user.

    GET: Retrieve a list of all users.
    POST: Create a new user.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint to retrieve, update, or delete a user by ID.

    GET: Retrieve a user by ID.
    PUT: Update a user by ID.
    PATCH: Partially update a user by ID.
    DELETE: Delete a user by ID.
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

# Category Endpoints

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all categories or create a new category.

    GET: Retrieve a list of all categories.
    POST: Create a new category.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint to retrieve, update, or delete a category by ID.

    GET: Retrieve a category by ID.
    PUT: Update a category by ID.
    PATCH: Partially update a category by ID.
    DELETE: Delete a category by ID.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

# Product Endpoints

# get products of category
class ProductByCategoryAPIView(generics.ListAPIView):
    ''' get the products of a category by the name of category'''

    serializer_class = ProductSerializer

    def get_queryset(self):
        category_name = self.kwargs['category_name']  # assuming category name is passed in URL
        queryset = Product.objects.filter(category__name=category_name)
        return queryset
    
class ProductListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all products or create a new product.

    GET: Retrieve a list of all products.
    POST: Create a new product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

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

# Cart Endpoints

class CartListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all carts or create a new cart.

    GET: Retrieve a list of all carts.
    POST: Create a new cart.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

class CartRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint to retrieve, update, or delete a cart by ID.

    GET: Retrieve a cart by ID.
    PUT: Update a cart by ID.
    PATCH: Partially update a cart by ID.
    DELETE: Delete a cart by ID.
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer

# CartItem Endpoints

class CartItemListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all cart items or create a new cart item.

    GET: Retrieve a list of all cart items.
    POST: Create a new cart item.
    """
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer



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

# Payment Endpoints

class PaymentListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all payments or create a new payment.

    GET: Retrieve a list of all payments.
    POST: Create a new payment.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class PaymentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Endpoint to retrieve, update, or delete a payment by ID.

    GET: Retrieve a payment by ID.
    PUT: Update a payment by ID.
    PATCH: Partially update a payment by ID.
    DELETE: Delete a payment by ID.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
