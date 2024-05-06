# urls.py
from django.contrib import admin
from django.urls import path
from back_api.views import (
    LogoutViewSet ,SignupViewSet ,LoginViewSet,
    CartItemListCreateAPIView,CartItemRetrieveUpdateDestroyAPIView,
    # add_to_cart,
    CategoryListCreateAPIView,ProductListCreateAPIView,
    # ProductByCategoryAPIView,
    UserProfileRetrieveUpdateAPIView,
    FavoriteListCreateAPIView,FavoriteRetrieveUpdateDestroyAPIView,
    CheckoutAPIView,index
    )
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    )


urlpatterns = [
    # path('', index, name='index'),
    path('api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    # path('token', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('admin/', admin.site.urls),
    path('signup', SignupViewSet.as_view({'post': 'signup'}), name='user-signup'),
    path('login', LoginViewSet.as_view({'post': 'login'}), name='user-login'),
    path('logout', LogoutViewSet.as_view({'post': 'logout'}), name='logout'),
    path('user', UserProfileRetrieveUpdateAPIView.as_view(), name='user-list-create'),
    path('categories', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('products', ProductListCreateAPIView.as_view(), name='product-list-create'),
    # path('products/search/', ProductListCreateAPIView.as_view(), name='product-search-by-name'),
    # path('products/categories/<str:category_name>/', ProductByCategoryAPIView.as_view(), name='products_by_category'),
    path('favorites', FavoriteListCreateAPIView.as_view(), name='favorite-list-create'),    
    path('favorites/<int:pk>', FavoriteRetrieveUpdateDestroyAPIView.as_view(), name='favorite-retrieve-update-destroy'),
    path('cartitem', CartItemListCreateAPIView.as_view(), name='cartitem-list-create'),
    # path('cartitem/', add_to_cart, name='cartitem-create'),
    path('cartitem/<int:pk>', CartItemRetrieveUpdateDestroyAPIView.as_view(), name='cartitem-detail'),
    path('checkout', CheckoutAPIView.as_view(), name='checkout'),
]