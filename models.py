from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Product model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

# Cart model (linked to a user)
class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Cart for {self.user.username}"

# CartItem model (links to Cart and Product or Image)
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, null=True, blank=True, on_delete=models.CASCADE)
    image = models.ForeignKey('Image', null=True, blank=True, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        if self.product:
            return self.product.price * self.quantity
        elif self.image:
            return self.image.price * self.quantity
        return 0

    def __str__(self):
        if self.product:
            return f"{self.quantity} of {self.product.name} in cart"
        elif self.image:
            return f"{self.quantity} of {self.image.name} in cart"
        return "Empty CartItem"

# Order model (stores order data)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    card = models.CharField(max_length=255, blank=True, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.user.username}, Total: {self.total_price}"
# UploadedImage model (for uploading additional images)
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Image model (additional images with pricing)
class Image(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name
