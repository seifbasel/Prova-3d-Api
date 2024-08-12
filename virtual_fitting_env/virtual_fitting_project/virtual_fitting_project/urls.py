# urls.py
from django import views
from django.contrib import admin
from django.urls import path
from back_api.views import (
    CartItemDeleteAPIView,
    CartTotalAPIView,
    CommentListCreateAPIView,
    CommentRetrieveUpdateDestroyAPIView,
    FavoriteDeleteAPIView,
    LogoutViewSet,
    ReviewListCreateAPIView,
    SignupViewSet,LoginViewSet,
    CartItemListCreateAPIView,
    CategoryListCreateAPIView,
    ProductListCreateAPIView,
    UserProfileRetrieveUpdateAPIView,
    FavoriteListCreateAPIView,
    CheckoutAPIView,ping
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
    )
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/admin/', admin.site.urls),
    path('api/signup', SignupViewSet.as_view({'post': 'signup'}), name='user-signup'),
    path('api/login', LoginViewSet.as_view({'post': 'login'}), name='user-login'),
    path('api/logout', LogoutViewSet.as_view({'post': 'logout'}), name='logout'),
    path('api/user', UserProfileRetrieveUpdateAPIView.as_view(), name='user-list-create'),
    path('api/categories', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('api/products', ProductListCreateAPIView.as_view(), name='product-list-create'),
    path('api/favorites', FavoriteListCreateAPIView.as_view(), name='favorite-list-create'),    
    path('api/favorites/delete', FavoriteDeleteAPIView.as_view(), name='favorite-delete'),
    path('api/cartitem', CartItemListCreateAPIView.as_view(), name='cartitem-list-create'),
    path('api/cartitem/delete', CartItemDeleteAPIView.as_view(), name='cart-item-delete'),
    path('api/carttotal', CartTotalAPIView.as_view(), name='cart-total'),
    path('api/checkout', CheckoutAPIView.as_view(), name='checkout'),
    path('api/products/<int:product_id>/comments/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
    path('api/comments/<int:pk>/', CommentRetrieveUpdateDestroyAPIView.as_view(), name='comment-detail'),
    
    path('api/review', ReviewListCreateAPIView.as_view(), name='review-list-create'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)