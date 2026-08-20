from django.contrib import admin
from .models import Order,OrderItem

#register your model here

admin.site.register(Order)
admin.site.register(OrderItem)


