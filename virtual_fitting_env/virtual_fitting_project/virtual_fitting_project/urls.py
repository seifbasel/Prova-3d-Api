# urls.py
from django.contrib import admin
from django.urls import include, path
from back_api.views import (
    CartItemListCreateAPIView, CartItemRetrieveUpdateDestroyAPIView,
    CartListCreateAPIView, CartRetrieveUpdateDestroyAPIView,
    CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView,
    PaymentListCreateAPIView, PaymentRetrieveUpdateDestroyAPIView,
    ProductListCreateAPIView, ProductRetrieveUpdateDestroyAPIView,ProductByCategoryAPIView,
    UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView
)
from back_api.views import CustomUserViewSet
# user_login,register_user
# ,UserLoginAPIView, UserRegistrationAPIView ,
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'users', CustomUserViewSet, basename='users')
# router.register(r'users', CustomUserViewSet)
# router.register(r'admin-profiles', AdminProfileViewSet)
# router.register(r'products', ProductListCreateAPIView)
# router.register(r'carts', CartListCreateAPIView)
# router.register(r'cart-items', CartItemListCreateAPIView)
# router.register(r'payments', PaymentListCreateAPIView)
# router.register(r'categories', CategoryListCreateAPIView)

urlpatterns = [
    # path('', include(router.urls)),
    path('admin/', admin.site.urls),
    # path('register/', register_user, name='user-register'),
    # path('login/', user_login, name='user-login'),
    path('login/', CustomUserViewSet.as_view({'post': 'login'}), name='user-login'),
    path('signup/', CustomUserViewSet.as_view({'post': 'signup'}), name='user-signup'),
    path('users/', UserListCreateAPIView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user-detail'),
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-detail'),
    path('products/', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='product-detail'),
    path('products/category/<str:category_name>/', ProductByCategoryAPIView.as_view(), name='products_by_category'),
    path('carts/', CartListCreateAPIView.as_view(), name='cart-list-create'),
    path('carts/<int:pk>/', CartRetrieveUpdateDestroyAPIView.as_view(), name='cart-detail'),
    path('cartitems/', CartItemListCreateAPIView.as_view(), name='cartitem-list-create'),
    path('cartitems/<int:pk>/', CartItemRetrieveUpdateDestroyAPIView.as_view(), name='cartitem-detail'),
    path('payments/', PaymentListCreateAPIView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/', PaymentRetrieveUpdateDestroyAPIView.as_view(), name='payment-detail'),
]


