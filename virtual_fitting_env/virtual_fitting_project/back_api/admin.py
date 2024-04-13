# Register your models here.

from django.contrib import admin
from .models import UserProfile, Category, Product, Cart, CartItem, Payment

admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Payment)
