# urls.py
from django.contrib import admin
from django.urls import include, path
from back_api.views import (
    CartItemListCreateAPIView, CartItemRetrieveUpdateDestroyAPIView,
    CartListCreateAPIView, CartRetrieveUpdateDestroyAPIView,
    CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView,
    PaymentListCreateAPIView, PaymentRetrieveUpdateDestroyAPIView,
    ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView,
    ProductByCategoryAPIView,UserListCreateAPIView, 
    UserRetrieveUpdateDestroyAPIView ,FavoriteListCreateAPIView,
    FavoriteRetrieveUpdateDestroyAPIView
    # ,UserProfileInfoAPIView

)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from back_api.views import LogoutViewSet ,SignupViewSet ,LoginViewSet
from rest_framework.routers import DefaultRouter
# from back_api.views import SignupAPIView, LoginAPIView, CustomTokenObtainPairView

# router = DefaultRouter()
# router.register(r'users', UserListCreateAPIView)
# router.register(r'products', ProductListCreateAPIView)
# router.register(r'carts', CartListCreateAPIView)
# router.register(r'cart-items', CartItemListCreateAPIView)
# router.register(r'payments', PaymentListCreateAPIView)
# router.register(r'categories', CategoryListCreateAPIView)
# router.register(r'signup', SignupViewSet, basename='signup')
# router.register(r'login', LoginViewSet, basename='login')
# router.register(r'logout', LogoutViewSet, basename='logout')

urlpatterns = [
    # path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('signup/', SignupAPIView.as_view(), name='signup'),
    # path('login/', LoginAPIView.as_view(), name='login'),
    # path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('admin/', admin.site.urls),
    path('signup/', SignupViewSet.as_view({'post': 'signup'}), name='user-signup'),
    path('login/', LoginViewSet.as_view({'post': 'login'}), name='user-login'),
    # path('logout/', LogoutViewSet.as_view(), name='user-logout'),
    # path('forgot-password/', forgot_password, name='forgot_password'),
    # path('reset-password/<str:uidb64>/<str:token>/', reset_password, name='reset_password'),
    # path('user/info/', UserProfileInfoAPIView.as_view(), name='user-info'),
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    # path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    path('products/category/<str:category_name>/', ProductByCategoryAPIView.as_view(), name='products_by_category'),
    path('favorites/', FavoriteListCreateAPIView.as_view(), name='favorite-list-create'),    
    path('favorites/<int:pk>/', FavoriteRetrieveUpdateDestroyAPIView.as_view(), name='favorite-retrieve-update-destroy'),
    path('carts/', CartListCreateAPIView.as_view(), name='cart-list-create'),
    path('carts/<int:pk>/', CartRetrieveUpdateDestroyAPIView.as_view(), name='cart-detail'),
    path('cartitems/', CartItemListCreateAPIView.as_view(), name='cartitem-list-create'),
    path('cartitems/<int:pk>/', CartItemRetrieveUpdateDestroyAPIView.as_view(), name='cartitem-detail'),
    path('payments/', PaymentListCreateAPIView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentRetrieveUpdateDestroyAPIView.as_view(), name='payment-detail'),
]


