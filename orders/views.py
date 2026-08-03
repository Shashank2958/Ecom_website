from django.http import JsonResponse
from django.shortcuts import render, redirect,get_object_or_404
from .models import Order, OrderItem
from products.models import Product
from django.conf import settings
import razorpay
import uuid



client=razorpay.Client(
    auth=(
        settings.RAZORPAY_KEY_ID,
        settings.RAZORPAY_KEY_SECRET
    )
)

def checkout(request):
    if request.method=="POST":
        
        
        name=request.POST.get("name")
        phone=request.POST.get("phone")
        address=request.POST.get("address")
        buy_now=request.session.get("buy_now")
        cart=request.session.get("cart",{})
        payment_method=request.POST.get("payment_method")
        
        
        
       
        
        #===========================================================
                            #buy flow
        #========================================================
        if buy_now:
            product=get_object_or_404(Product,id=buy_now["product_id"])
            quantity=buy_now["quantity"]
            
            total= product.retail_price*quantity
            
            
            if payment_method=="COD":
                            
                            
                
                order=Order.objects.create(
                    name=name,
                    phone=phone,
                    address=address,
                    total=total,
                    payment_method=payment_method
                )        
                
                
                
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=quantity,
                    price=product.retail_price
                    
                )
                del request.session["buy_now"]
                return redirect('order-success')
        
        
            elif payment_method=="ONLINE":
                request.session["checkout_data"]={
                    "name":name,
                    "phone":phone,
                    "address":address,
                    "total":float(total),
                    "payment_method":payment_method,
                    "buy_now":buy_now,
                }
                
                receipt= str(uuid.uuid4())
               
                
                razorpay_order= client.order.create({
                        "amount":int(total*100),
                        "currency":"INR",
                        "receipt":receipt,
                }
                )
                
                razorpay_order_id=razorpay_order["id"]
                
                ##json response
                
                return JsonResponse({
                    "razorpay_order_id":razorpay_order_id,
                    "key":settings.RAZORPAY_KEY_ID,
                    "amount":int(total*100),
                })
            
    
            
            
        
        #cart-flow
        else:
            
            total = sum(
                item["price"] * item["quantity"]
                for item in cart.values()
            )
            
            
            
            if payment_method=="COD":
                
                
            
                order=Order.objects.create(
                    name=name,
                    phone=phone,
                    address=address,
                    total=total,
                    payment_method=payment_method
                )        
                print(order.id)
                
                for product_id, item in cart.items():
                    product = get_object_or_404(Product, id=product_id)
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        quantity=item["quantity"],
                        price=item["price"]
                        
                    )
                request.session["cart"] = {}
                return redirect('order-success')
        
        
            elif payment_method=="ONLINE":
                request.session["checkout_data"]={
                    "name":name,
                    "phone":phone,
                    "address":address,
                    "total":float(total),
                    "payment_method":payment_method,
                    "cart":cart,
                }
                
                receipt= str(uuid.uuid4())
               
                
                razorpay_order= client.order.create({
                        "amount":int(total*100),
                        "currency":"INR",
                        "receipt":receipt,
                }
                )
                
                razorpay_order_id=razorpay_order["id"]
                
                ##json response
                
                return JsonResponse({
                    "razorpay_order_id":razorpay_order_id,
                    "key":settings.RAZORPAY_KEY_ID,
                    "amount":int(total*100),
                })
        
    return render(request,'checkout.html')

def verify_payment(request):
    razorpay_payment_id= request.POST.get(razorpay_payment_id)
    razorpay_order_id= request.POST.get(razorpay_order_id)
    razorpay_signature= request.POST.get(razorpay_signature)
    
    client.utility.verify_payment_signature(razorpay_signature)
    
    


def order_success(request):
    return render(request,"success.html")