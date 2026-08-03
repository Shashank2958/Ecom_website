from django.urls import path
from . import views

urlpatterns=[
    path('checkout/', views.checkout,name='checkout'),
    path('verify-paymnt/', views.verify_payment,name='verify_payment'),
    path('order-success/', views.order_success,name='order-success'),

    
]

   