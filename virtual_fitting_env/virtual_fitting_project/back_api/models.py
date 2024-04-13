from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db import models



class CustomUser(AbstractUser):
    # Your custom fields here
    phone_number = models.CharField(max_length=15)
    address = models.TextField() 
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)

    # Specify unique related_name arguments to avoid clashes
    groups = models.ManyToManyField('auth.Group', related_name='custom_user_groups')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='custom_user_permissions')

    def __str__(self):
        return self.username


class AdminProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    contact_number = models.CharField(max_length=20)
    role = models.CharField(max_length=50)

    def __str__(self):
        return f"Admin Profile for {self.user.username}"

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)  
    brand = models.CharField(max_length=100)
    size = models.CharField(max_length=10)  
    color = models.CharField(max_length=50)
    image = models.ImageField(upload_to='product_images/')  

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Consider removing the one-to-one constraint and adding additional fields as needed


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        unique_together = ['cart', 'product']  # Ensure each product is added to the cart only once


class Payment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment #{self.id} - {self.amount} {self.currency} ({self.status})"
