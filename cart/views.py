from django.shortcuts import render,redirect,get_object_or_404
from products.models import Product
from django.contrib import messages

# Create your views here.
def add_to_cart(request,product_id):
    product=get_object_or_404(Product,id=product_id)
    cart = request.session.get('cart',{})
    if str(product_id) in cart:
        cart[str(product_id)]['quantity'] +=1
    else:
        cart[str(product_id)]={
            'name':product.name,
            'price':float(product.retail_price),
            'quantity': 1,
            'image':product.image.url,
        }
    request.session['cart']=cart
    messages.success(request,"Product added to cart successfully!")
    return redirect('products_details',id=product_id)

def cart_detail(request):
    cart=request.session.get('cart',{})
    total=sum(item['price']*item['quantity'] for item in cart.values())
    
    return render(request,'cart.html', {
        'cart':cart,
        'total':total
    })
    
def increase_quantity(request,product_id):
    cart=request.session.get('cart',{})
    if (str(product_id) in cart):
        cart[str(product_id)]['quantity']+=1
    request.session['cart']=cart
    return redirect('cart_detail')

def decrease_quantity(request,product_id):
    cart=request.session.get('cart',{})
    if str(product_id) in cart:
        if cart[str(product_id)]['quantity']>1:
            cart[str(product_id)]['quantity']-=1
    request.session['cart']=cart
    return redirect('cart_detail')

def remove_from_cart(request,product_id):
    cart=request.session.get('cart',{})
    if str(product_id) in cart:
        del cart[str(product_id)]
    request.session['cart']=cart
    return redirect('cart_detail')
