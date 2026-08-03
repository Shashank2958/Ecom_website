from django.urls import path
from . import views

urlpatterns=[
    path('/products', views.products,name='products'),
    path('<int:id>/', views.products_details,name='products_details'),
    path('buy-now/<int:product_id>/', views.buy_now,name='buy_now'),
    
]