from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15 ,blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='users_images/',null=True,blank=True)  

    def __str__(self):
        return str(self.user)

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
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('k', 'Kids'),
        ('B', 'Both'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    brand = models.CharField(max_length=100)
    SIZE_CHOICES = (
            ('S', 'S'),
            ('M', 'M'),
            ('L', 'L'),
            ('XL', 'XL'),
            ('XXL', 'XXL'),
        )
    size = models.CharField(max_length=10,choices=SIZE_CHOICES)    
    color = models.CharField(max_length=50)
    # image = models.ImageField(upload_to='product_images/')
    image =models.CharField()
    lens_id=models.CharField(max_length=200,null=True,blank=True)
    lens_group_id=models.CharField(max_length=200,null=True,blank=True)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    def sentiment_to_stars(self, sentiment):
        """
        Converts sentiment score to star rating.
        Assumes sentiment ranges from 0 (negative) to 1 (positive).
        Maps this to a 1 to 5 star rating.
        """
        return int(sentiment * 4 + 1)  # Maps 0 to 1 to 1 to 5

    def update_rating(self):
        comments = self.comments.all()
        if comments:
            total_stars = sum(self.sentiment_to_stars(comment.sentiment) for comment in comments if comment.sentiment is not None)
            self.rating = round(total_stars / comments.count())
        else:
            self.rating = 0
        self.save()

class Favorite(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')  # Ensure each user can only have one favorite entry per product

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"

@receiver(post_save, sender=UserProfile)
def create_cart_for_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create a cart for a user profile when it is created.
    """
    if created:
        # Create a cart for the user profile
        Cart.objects.create(user=instance)

class Cart(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)+' '+'cart'

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)  # Default to 1 when a new cart item is created

    class Meta:
        unique_together = ['cart', 'product']  # Ensure each product is added to the cart only once
    
    def __str__(self):
        return f"Owner: {self.cart.user.user.username}, Product: {self.product.name}"

class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    ORDER_STATUS_CHOICES = (
    ('Pending', 'Pending'),
    ('Processing', 'Processing'),
    ('Shipped', 'Shipped'),
    ('Delivered', 'Delivered'),
    ('Cancelled', 'Cancelled'),)
    status = models.CharField(max_length=100, choices=ORDER_STATUS_CHOICES)
    shipping_address = models.TextField()
    # created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"Owner: {self.user.user.username}"

class Comment(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    sentiment = models.IntegerField(null=True)  # Add sentiment field here
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text
    
@receiver(post_save, sender=Comment)
def update_product_rating_on_save(sender, instance, **kwargs):
    instance.product.update_rating()

@receiver(post_delete, sender=Comment)
def update_product_rating_on_delete(sender, instance, **kwargs):
    instance.product.update_rating()

class review(models.Model):
    
    text = models.TextField()
    sentiment = models.IntegerField(null=True)  # Add sentiment field here

    def __str__(self):
        return self.text