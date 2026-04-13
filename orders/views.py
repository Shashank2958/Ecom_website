from django.shortcuts import render, redirect
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import razorpay, json
from .models import Order, Product, OrderItem


@csrf_exempt
def checkout(request):

    cart = request.session.get('cart', {})
    total = sum(item['price'] * item['quantity'] for item in cart.values())

    # ===============================
    # 🟢 STEP 1: ORDER CREATE (FORM)
    # ===============================
    if request.method == "POST" and request.POST.get('name'):

        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(
            name=request.POST.get('name'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            total_amount=total,
            payment_method=payment_method
        )

        # 🟢 Save Order Items
        for key, item in cart.items():
            product = Product.objects.get(id=key)
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['price']
            )

        # 🟢 COD CASE
        if payment_method == "cod":
            order.status = "confirmed"
            order.payment_status = "pending"
            order.save()

            request.session['cart'] = {}
            return redirect('order_success')

        # 🟢 ONLINE PAYMENT
        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        payment = client.order.create({
            "amount": total * 100,
            "currency": "INR",
            "payment_capture": 1
        })

        order.razorpay_order_id = payment['id']
        order.save()

        return render(request, "payment.html", {
            "razorpay_key": settings.RAZORPAY_KEY_ID,
            "amount": total * 100,
            "razorpay_order_id": payment['id']
        })

    # ===============================
    # 🟢 STEP 2: PAYMENT VERIFY
    # ===============================
    if request.method == "POST" and request.body:

        data = json.loads(request.body)

        client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': data['razorpay_order_id'],
                'razorpay_payment_id': data['razorpay_payment_id'],
                'razorpay_signature': data['razorpay_signature']
            })

            order = Order.objects.get(
                razorpay_order_id=data['razorpay_order_id']
            )

            order.payment_status = "paid"
            order.status = "confirmed"
            order.save()

            request.session['cart'] = {}

            return JsonResponse({"status": "success"})

        except:
            return JsonResponse({"status": "failed"})

    return render(request, "checkout.html", {"total": total})


# ===============================
# 🟢 WEBHOOK (BACKUP)
# ===============================
@csrf_exempt
def razorpay_webhook(request):

    try:
        payload = json.loads(request.body)

        if payload['event'] == "payment.captured":

            order_id = payload['payload']['payment']['entity']['order_id']

            order = Order.objects.get(razorpay_order_id=order_id)

            order.payment_status = "paid"
            order.status = "confirmed"
            order.save()

        return JsonResponse({"status": "ok"})

    except:
        return JsonResponse({"status": "failed"})

def order_success(request):
    return render(request, 'success.html')
