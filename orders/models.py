from django.db import models
from products.models import Product

# Create your models here.
class Order(models.Model):
    name= models.CharField(max_length=200)
    phone= models.CharField(max_length=15)
    address= models.TextField()
    total_amount=models.PositiveIntegerField()
    
    PAYMENT_METHOD_CHOICES=[
        ('cod','Cash on Delivery'),
        ('online', 'Online Payment')]
    
        
    
    PAYMENT_STATUS_CHOICES=[
        ('pending','Pending'),
        ('paid','Paid'),
        ('failed','Failed'),
    ]
    
    #Status choice(tracking ke liye)
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('confirmed','Confirmed'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
        
    ]
    # Payment info
    payment_method=models.CharField(max_length=20,choices=PAYMENT_METHOD_CHOICES)
    payment_status=models.CharField(max_length=20,choices=PAYMENT_STATUS_CHOICES,default='pending')
    
    #razorpay fields
    
    razorpay_order_id=models.CharField(max_length=255,blank=True,null=True)
    razorpay_payment_id=models.CharField(max_length=255,blank=True,null=True)
    razorpay_signature=models.CharField(max_length=255,blank=True,null=True)
    
    #status(order tracking)
    
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')

    
    created_at=models.DateTimeField(auto_now_add=True)
    
     
    def __str__(self):
        return f"order #{self.id}-{self.name}"
    
class OrderItem(models.Model):
    order= models.ForeignKey(Order,on_delete=models.CASCADE)
    product= models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    price=models.FloatField()
    
    def __str__(self):
        return f"{self.product.name} ({self.quantity})"