# views.py
from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from rest_framework import generics, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserProfile, Category, Product, Cart, CartItem, Payment ,Favorite
from .serializers import UserProfileSerializer, CategorySerializer, ProductSerializer,FavoriteSerializer,CartSerializer, CartItemSerializer, PaymentSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny,IsAdminUser
from back_api.permission import IsAdminOrReadOnly 
from django.shortcuts import get_object_or_404



# class SignupViewSet(viewsets.ViewSet):
#     """
#     View set to handle user signup.
#     """
#     @action(detail=False, methods=['post'], permission_classes=[AllowAny])
#     def signup(self, request):
#         """
#         Create a new user and generate a token.

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

#         if not all([username, email, password]):
#             return Response({'error': 'Username, email, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             user = User.objects.create_user(username=username, email=email, password=password)
#             token, _ = Token.objects.get_or_create(user=user)  # Generate token
#             return Response({'message': 'User registered successfully', 'token': token.key}, status=status.HTTP_201_CREATED)
#         except IntegrityError:
#             return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)


# class LoginViewSet(viewsets.ViewSet):
#     """
#     View set to handle user login.
#     """
#     @action(detail=False, methods=['post'], permission_classes=[AllowAny])
#     def login(self, request):
#         """
#         Authenticate a user and generate an authentication token.

#         Parameters:
#         - username: The username of the user.
#         - password: The password of the user.

#         Returns:
#         - A response containing an authentication token if authentication succeeds, or an error message if authentication fails.
#         """
#         username = request.data.get('username')
#         password = request.data.get('password')

#         if not all([username, password]):
#             return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(username=username, password=password)

#         if user:
#             token, _ = Token.objects.get_or_create(user=user)
#             return Response({'token': token.key}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        

# views.py

from rest_framework_simplejwt.tokens import RefreshToken

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
            refresh = RefreshToken.for_user(user)
            return Response({'message': 'User registered successfully', 'access': str(refresh.access_token)}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'Username or email already exists'}, status=status.HTTP_400_BAD_REQUEST)


class LoginViewSet(viewsets.ViewSet):
    """
    View set to handle user login.
    """
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        """
        Authenticate a user and generate a JWT token.

        Parameters:
        - username: The username of the user.
        - password: The password of the user.

        Returns:
        - A response containing a JWT access token if authentication succeeds, or an error message if authentication fails.
        """
        username = request.data.get('username')
        password = request.data.get('password')

        if not all([username, password]):
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)



from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout

class LogoutViewSet(viewsets.ViewSet):
    """
    View set to handle user logout.
    """
    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """
        Log out the current user.

        Returns:
        - A response indicating success or failure of the logout process.
        """
        logout(request)
        return Response({'message': 'User logged out successfully'}, status=status.HTTP_200_OK)


# from rest_framework.views import APIView

# class UserProfileInfoAPIView(APIView):
#     """
#     Endpoint to retrieve all information related to the logged-in user.
#     """

#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         # Retrieve user's profile
#         user_profile = UserProfileSerializer(request.user.profile).data

#         # Retrieve user's favorite products
#         favorite_products = Favorite.objects.filter(user=request.user)
#         favorite_products_data = FavoriteSerializer(favorite_products, many=True).data

#         # Retrieve user's cart items
#         cart_items = CartItem.objects.filter(cart__user=request.user)
#         cart_items_data = CartItemSerializer(cart_items, many=True).data

#         # Retrieve user's payments
#         payments = Payment.objects.filter(user=request.user)
#         payments_data = PaymentSerializer(payments, many=True).data

#         # Compile all data
#         user_info = {
#             'profile': user_profile,
#             'favorite_products': favorite_products_data,
#             'cart_items': cart_items_data,
#             'payments': payments_data
#         }

#         return Response(user_info)


class UserListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all users or create a new user.

    GET: Retrieve the current user's profile.
    POST: Create a new user.
    """
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]  # Allow only authenticated users

    def get_queryset(self):
        """
        Return the queryset of UserProfile filtered by the current user.
        """
        return UserProfile.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """
        Associate the new user's profile with the current user.
        """
        serializer.save(user=self.request.user)


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
    permission_classes = [IsAdminUser]  # Restrict access to admin users only


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
    permission_classes = [IsAdminOrReadOnly]


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
    permission_classes = [IsAdminOrReadOnly]  # Restrict access to authenticated users only


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
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only


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

class CartListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all carts or create a new cart.

    GET: Retrieve a list of all carts.
    POST: Create a new cart.
    """
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only

    def get_queryset(self):
        # Get the UserProfile instance associated with the current user
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        # Filter carts based on the current user profile
        return Cart.objects.filter(user=user_profile)

    def perform_create(self, serializer):
        # Get the UserProfile instance associated with the current user
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        # Associate the cart with the current user profile during creation
        serializer.save(user=user_profile)


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
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only

    def get_queryset(self):
        # Get the UserProfile instance associated with the current user
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        # Filter carts based on the current user profile
        return Cart.objects.filter(user=user_profile)



# CartItem Endpoints

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
        # Get the UserProfile instance associated with the current user
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        # Filter cart items based on the current user's cart
        return CartItem.objects.filter(cart__user=user_profile)

    def perform_create(self, serializer):
        # Get the UserProfile instance associated with the current user
        user_profile = get_object_or_404(UserProfile, user=self.request.user)
        # Get the user's cart
        cart = Cart.objects.get(user=user_profile)
        # Associate the cart item with the current user's cart during creation
        serializer.save(cart=cart)

  


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


# Payment Endpoints

class PaymentListCreateAPIView(generics.ListCreateAPIView):
    """
    Endpoint to list all payments or create a new payment.

    GET: Retrieve a list of all payments.
    POST: Create a new payment.
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only

    def perform_create(self, serializer):
        # Associate the payment with the current user during creation
        serializer.save(user=self.request.user)



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
    permission_classes = [IsAuthenticated]  # Restrict access to authenticated users only