from django.db import models

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    image=models.ImageField(upload_to='categories/',blank=True,null=True)
    is_active=models.BooleanField(default=True)
    
    def __str__(self):
        return self.name
        
class Product(models.Model):
    category=models.ForeignKey(Category,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)
    Description=models.TextField(blank=True)
    retail_price=models.DecimalField(max_digits=10,decimal_places=2)
    wholesale_price=models.DecimalField(max_digits=10,decimal_places=2,blank=True,null=True)
    image=models.ImageField(upload_to='products/')
    is_available=models.BooleanField(default=True)
    
    def __str__(self):
        return self.name