from django.urls import path
from . import views

urlpatterns=[
    path('checkout/', views.checkout,name='checkout'),
    path('verify-payment/', views.verify_payment,name='verify-payment'),
    path('order-success/', views.order_success,name='order-success'),
    path('webhook/', views.razorpay_webhook,name='razorpay_webhook')

    
]

   