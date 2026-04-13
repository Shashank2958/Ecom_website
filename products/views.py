from django.shortcuts import render , get_object_or_404
from .models import Product

# Create your views here.
def products(request):
    products=Product.objects.filter(is_available=True)
    return render(request,'products.html',{'products':products})    

def products_details(request,id):
    product= get_object_or_404(Product,id=id)
    return render(request,'products_details.html',{'product':product})
    