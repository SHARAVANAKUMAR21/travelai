from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings


# models.py
from django.db import models

class Person(models.Model):
    fullname = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10)  # You can use choices for Male, Female, Other
    order = models.ForeignKey('Order', on_delete=models.CASCADE)  # Assuming you have an Order model

    def __str__(self):
        return self.fullname



class UserProfile(AbstractUser):
    age = models.PositiveIntegerField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)  # Nullable email field

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='user_profiles',  # Custom related name to avoid clashes
        related_query_name='user_profile',
        blank=True,
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='user_profiles',  # Custom related name to avoid clashes
        related_query_name='user_profile',
        blank=True,
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     parent = models.ForeignKey('self', null=True, blank=True, related_name='subcategories', on_delete=models.CASCADE)

#     def __str__(self):
#         return self.name

class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    quantity = models.IntegerField(default=0)
    reorderlevel = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def is_at_reorder_level(self):
        return self.quantity <= self.reorderlevel

    def clean(self):
        if self.price < 0:
            raise ValidationErr('Price cannot be negative.')
        if self.quantity < 0:
            raise ValidationErr('Quantity cannot be negative.')
        if self.reorderlevel < 0:
            raise ValidationErr('Reorder level cannot be negative.')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']  # Orders by name alphabetically


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use settings.AUTH_USER_MODEL
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"Cart for {self.user.username}: {self.product.name}"


from django.conf import settings
from django.db import models

class Order(models.Model):
    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('out_for_delivery', 'Out for Delivery'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='processing')
    created_at = models.DateTimeField(auto_now_add=True)
    delivered_at = models.DateTimeField(null=True, blank=True)  # Optional field for tracking delivery time

    def __str__(self):
        return f"Order for {self.fullname} placed on {self.created_at}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)  # Set a default value

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"


class Supplier(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    contact_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=100, unique=True)  # Added unique constraint
    company_name = models.CharField(max_length=100)
    company_website = models.URLField(max_length=200)
    delivery_date = models.DateField(default=timezone.now)

    def __str__(self):  # Corrected the method name
        return f"{self.company_name} (ID: {self.pk})"


class SupplierOrder(models.Model):
    STATUS_CHOICES = [
        ('can be satisfied', 'Can be Satisfied'),
        ('stock not available', 'Stock Not Available'),
    ]

    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date_of_order = models.DateField(default=timezone.now)
    delivery_date = models.DateField()
    date_of_delivery = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='can be satisfied')  # Adjusted default status

    def __str__(self):
        return f"Order {self.pk} for {self.product.name} from {self.supplier.company_name}"
    
    


from django.contrib.auth.models import User
    

class ChatHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message_input = models.TextField()
    bot_response = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"{self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
    
    

