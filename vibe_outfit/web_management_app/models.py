from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


# --------------------------- navigation bar start here ---------------------------
class CompanyLogo(models.Model):
    logo = models.ImageField( upload_to='assets/', blank=False, null= False)
    url = models.URLField(max_length=300)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        verbose_name = "Company Logo"
        verbose_name_plural = "Company Logos"

class NavOption(models.Model):
    title = models.CharField(max_length=50)
    url = models.URLField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Navigation Options"
        verbose_name_plural = "Navigation Options"

class NavButtons(models.Model):
    icon = models.ImageField(upload_to='assets/', blank=False, null= False)
    url = models.URLField(max_length=300)
    order = models.PositiveIntegerField(default=0)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    
    class Meta:
        verbose_name = "Navigation Buttons"
        verbose_name_plural = "Navigation Buttons"

# --------------------------- navigation bar end here ---------------------------

# --------------------------- hero section bar start here ---------------------------
class HeroSection(models.Model):
    bg_img = models.ImageField(upload_to= 'assets/', blank= True, null= True)
    catalog_name = models.CharField(max_length= 100, blank= True, null= True)

    heading = models.CharField(max_length= 200, blank= False, null= False)
    sub_heading = models.CharField(max_length= 300, blank= False, null= False)

    cta_btn_1 = models.CharField(max_length=50, blank= False, null= False)
    cta_btn_1_url = models.URLField(max_length=300, blank= False, null= False)
    cta_btn_2 = models.CharField(max_length=50, blank= False, null= False)
    cta_btn_2_url = models.URLField(max_length=300, blank= False, null= False)

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero Section"
        verbose_name_plural = "Hero Section"

# --------------------------- hero section bar end here ---------------------------

# --------------------------- Product Section bar end here ---------------------------
class ProductCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, unique=True)
    order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to= 'catagory/',null=True, blank=True)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null= True, blank=True, related_name='children')

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Category's"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255, null= False, blank= False)
    slug = models.SlugField(max_length=255, unique=True)
    short_description = models.TextField()
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, related_name='products')

    featured_products = models.BooleanField(default=False)
    new_arrivals = models.BooleanField(default=False)


    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return self.name

class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to= 'products/', null=True, blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Image"
        verbose_name_plural = "Product Images"

class ProductReview(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(max_length=400)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Review"
        verbose_name_plural = "Product Review"
        unique_together = ['product', 'user']


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    sku = models.CharField(max_length=100, unique=True)
    
    # Flexible attribute fields - store any value
    color = models.CharField(max_length=50, blank=True, help_text="hex color #000000")
    size = models.CharField( max_length=20,  blank=True, help_text="e.g., S, M, L, XL, 38, 40, 42" )
    material = models.CharField( max_length=50,  blank=True, help_text="e.g., Cotton, Leather, Wood" )
    
    # Price: NULL means use product price
    # price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,help_text="Leave empty to use product price" )
    
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Product Variant"
        verbose_name_plural = "Product Variants"
        unique_together = ['product', 'color', 'size', 'material']
        indexes = [
            models.Index(fields=['sku']),
            models.Index(fields=['is_active']),
        ]
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Cart"
        verbose_name_plural = "Carts"
    
    def __str__(self):
        return f"Cart #{self.id} - {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        verbose_name = "Cart Item"
        verbose_name_plural = "Cart Items"
        unique_together = ['cart', 'variant']
    
    def __str__(self):
        return f"{self.quantity} x {self.variant.sku}"
    
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    # Payment method choices
    PAYMENT_METHOD_CHOICES = [
        ('credit_card', 'Credit Card'),
        ('debit_card', 'Debit Card'),
        ('paypal', 'PayPal'),
        ('stripe', 'Stripe'),
        ('cash_on_delivery', 'Cash on Delivery'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=30, choices= PAYMENT_METHOD_CHOICES, default='credit_card')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='items')
    
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# --------------------------- Product Section bar end here ---------------------------
