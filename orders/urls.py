from django.urls import path
from . import views

urlpatterns=[
    path('checkout/',views.checkout,name='checkout'),
   
    path('razorpay-webhook/', views.razorpay_webhook),
    path('success/',views.order_success,name='order_success'),
]

   