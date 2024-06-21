from django.contrib import admin
from .models import (
    UserProfile, Category,
    Product,Favorite,Cart,
    CartItem,Order,Comment,
    review)

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Favorite)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)          
admin.site.register(Comment)          
admin.site.register(review)
