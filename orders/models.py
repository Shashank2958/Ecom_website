from django.db import models
from products.models import Product

# Create your models here.
class Order(models.Model):
    
    PAYMENT_CHOICES=[
        ("COD","Cash on Delivery"),
        ("ONLINE","Online payment"),
    ]
    STATUS_CHOICES=[
        ("pending","Pending"),
        ("confirmed","confirmed"),
        ("shipped","shipped"),
        ("delivered","delivered"),
        ("cancelled","cancelled"),
    ]
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=15)
    address=models.TextField()
    
    total=models.DecimalField(max_digits=10,decimal_places=2)
    
    payment_method=models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default="COD"
    )
    
    status= models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
        
    )
    PAYMENT_STATUS_CHOICES=[
        ("pending","Pending"),
        ("paid","Paid"),
        ("failed","Failed"),
        ("refunded","Refunded"),
    ]
    payment_status=models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default="pending",
        
    )
    
    razorpay_order_id=models.CharField(
        max_length=100,
        blank=True,
        null=True
        )
    
    razorpay_payment_id= models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    razorpay_signature=models.CharField(
        max_length=255,
        blank=True,
        null=True
    )
    
    
    created_at= models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"order #{self.id}- {self.name}"
    
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveBigIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"