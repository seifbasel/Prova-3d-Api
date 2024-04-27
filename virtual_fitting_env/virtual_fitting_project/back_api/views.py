# views.py
from django.contrib.auth import authenticate, get_user_model
from django.db import IntegrityError
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import UserProfile, Category, Product, Cart, CartItem ,Favorite
from .serializers import UserProfileSerializer, CategorySerializer, ProductSerializer,FavoriteSerializer,CartSerializer, CartItemSerializer
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
            
            # Create a cart for the user
            # Cart.objects.create(user=user)

            # Generate a JWT token
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


# class LogoutViewSet(viewsets.ViewSet):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     @action(detail=False, methods=['post'], permission_classes=[AllowAny])
#     def logout(self, request):
#         refresh_token = request.data.get('refresh_token')

#         if not refresh_token:
#             return Response({'error': 'Refresh token is required'}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             # Verify the provided refresh token
#             token = RefreshToken(refresh_token)
#             token.verify()
            
#             # Blacklist the refresh token to invalidate the session
#             token.blacklist()

#             # Generate a new pair of access and refresh tokens
#             user = request.user
#             new_refresh = RefreshToken.for_user(user)
#             new_access = new_refresh.access_token

#             # Return the new tokens to the user
#             return Response({
#                 'access': str(new_access),
#                 'refresh': str(new_refresh)
#             }, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'error': 'Failed to logout'}, status=status.HTTP_400_BAD_REQUEST)




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

    def get_queryset(self):
        queryset = super().get_queryset()
        name = self.request.query_params.get('name')
        if name:
            queryset = queryset.filter(name__icontains=name)
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


# # views.py
# @api_view(['POST'])
# @authentication_classes([JWTAuthentication])
# @permission_classes([IsAuthenticated])
# def add_to_favorites(request):
#     serializer = FavoriteSerializer(data=request.data, context={'request': request})
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['POST'])
@authentication_classes([JWTAuthentication])  # Use JWT authentication
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def add_to_cart(request):
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

        return Response({'success': 'Product added to cart'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    

from django.db import transaction
from back_api.models import Order,OrderItem

@transaction.atomic
def checkout(request):
    # Get the user's cart
    cart_items = CartItem.objects.filter(cart__user=request.user)

    # Calculate total price
    total_price = sum(item.product.price * item.quantity for item in cart_items)

    # Create a new order
    order = Order.objects.create(
        user=request.user,
        total_price=total_price,
        status='Pending',  # Or any other initial status
        shipping_address=request.data.get('shipping_address')
    )

    # Add products from the cart to the order
    for item in cart_items:
        OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

    # Update product quantities and delete cart items
    for item in cart_items:
        product = item.product
        product.quantity -= item.quantity
        product.save()
        item.delete()

    return Response({'message': 'Order placed successfully'}, status=status.HTTP_201_CREATED)
