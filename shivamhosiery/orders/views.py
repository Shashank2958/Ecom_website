import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse,HttpResponse
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
            
            
           
                            
                            
                
            order=Order.objects.create(
                name=name,
                phone=phone,
                address=address,
                total=total,
                payment_method=payment_method,
                payment_status="pending",
                order_status="confirmed" if payment_method=="COD" else "pending"
                )        
                
                
                
                
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price=product.retail_price
                
            )
            
            if payment_method=="COD":
                
                del request.session["buy_now"]
                return redirect('order-success')
        
        
            elif payment_method=="ONLINE":
                
                receipt= str(uuid.uuid4())
               
                
                razorpay_order= client.order.create({
                        "amount":int(total*100),
                        "currency":"INR",
                        "receipt":receipt,
                }
                )
                
                order.razorpay_order_id=razorpay_order["id"]
                order.save()
                
                ##json response
                
                return JsonResponse({
                    "razorpay_order_id":order.razorpay_order_id,
                    "key":settings.RAZORPAY_KEY_ID,
                    "amount":int(total*100),
                })
            
    
            
            
        
        #cart-flow
        else:
            
            total = sum(
                item["price"] * item["quantity"]
                for item in cart.values()
            )
            
            
            
            
                
                
            
            order=Order.objects.create(
                name=name,
                phone=phone,
                address=address,
                total=total,
                payment_method=payment_method,
                payment_status="pending",
                order_status="confirmed" if payment_method =="COD" else "pending",
            )        
            
            
            for product_id, item in cart.items():
                product = get_object_or_404(Product, id=product_id)
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item["quantity"],
                    price=item["price"]
                    
                )
            if payment_method== "COD":
                request.session["cart"] = {}
                return redirect('order-success')
        
        
            elif payment_method=="ONLINE":
               
                receipt= str(uuid.uuid4())
               
                
                razorpay_order= client.order.create({
                        "amount":int(total*100),
                        "currency":"INR",
                        "receipt":receipt,
                }
                )
                
                order.razorpay_order_id=razorpay_order["id"]
                order.save()
                
                ##json response
                
                return JsonResponse({
                    "razorpay_order_id":order.razorpay_order_id,
                    "key":settings.RAZORPAY_KEY_ID,
                    "amount":int(total*100),
                })
        
    return render(request,'checkout.html')

def verify_payment(request):
    if request.method!="POST":
        return JsonResponse({
            "success":False,
            "message":"Method Not Allowed"
        },
        status=405
        
        )
    razorpay_payment_id= request.POST.get("razorpay_payment_id")
    razorpay_order_id= request.POST.get("razorpay_order_id")
    razorpay_signature= request.POST.get("razorpay_signature")
    
    try:
        
        order=Order.objects.get(razorpay_order_id=razorpay_order_id)
        
        if order.payment_status=="paid":
            return JsonResponse({
                "success":True,
                "message":"payment already verified"
            }
            )   
        client.utility.verify_payment_signature({
            "razorpay_order_id":razorpay_order_id,
            "razorpay_payment_id":razorpay_payment_id,
            "razorpay_signature":razorpay_signature,
        })
        #database update
        order.razorpay_payment_id=razorpay_payment_id
        order.razorpay_signature=razorpay_signature
        order.payment_status="paid"
        order.order_status="confirmed"
        order.save()
        
        return JsonResponse({
            "success":True,
            "message":"payment verified successfully"
        })
    except Order.DoesNotExist:
        return JsonResponse({
            "success":False,
            "message":"Order not found"
        },status=404)
    except razorpay.errors.SignatureVerificationError:
        return JsonResponse({
            "success":False,
            "message":"Invalid signature"
        },status=400)
    
    except Exception as e:

        return JsonResponse({
            "success": False,
            "message": str(e)
        }, status=500)
@csrf_exempt      
def razorpay_webhook(request):
    if request.method!= "POST":
        return HttpResponse(status=405)
    
    
    payload=request.body
    signature=request.headers.get("X-Razorpay-Signature")
    try:
        #webhook signature verification
        client.utility.verify_webhook_signature(
            payload,
            signature,
            settings.RAZORPAY_WEBHOOK_SECRET
        )
        
        data=json.loads(payload)
        
        event=data["event"]
        
        payment=data["payload"]["payment"]["entity"]
        
        razorpay_order_id=payment["order_id"]
        razorpay_payment_id=payment["id"]
        
        order=Order.objects.get(razorpay_order_id=razorpay_order_id)
        
        if event =="payment.captured":
            
            if order.payment_status!="paid":
                order.payment_status= "paid"
                order.order_status = "confirmed"
                order.razorpay_payment_id = razorpay_payment_id
                order.razorpay_signature = signature
                
                order.save()
        elif event == "payment.failed":
            if order.payment_status != "failed":
                order.payment_status = "failed"
                order.order_status = "pending"
                order.razorpay_payment_id = razorpay_payment_id
                order.razorpay_signature = signature

                order.save()
        
        return HttpResponse(status=200)
    
    except Order.DoesNotExist:
        return HttpResponse(status=404)
    
    except razorpay.errors.SignatureVerificationError:
        return HttpResponse(status=400)
    
    except Exception:
        return HttpResponse(status=500)


def order_success(request):
    return render(request,"success.html")