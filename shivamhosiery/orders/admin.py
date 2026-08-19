from django.contrib import admin
from django.utils.html import format_html
from .models import Order,OrderItem

#register your model here

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    
    list_display=(
        "id",
        "customer_name",
        "phone", 
        "total",
        "payment_method",
        "payment_status_badge",
        "order_status_badge",
        "created_at",
    )
    
    list_filter=(
        "payment_status",
        "order_status",
        "payment_method",
        "created_at",
    )
    search_fields=(
        "name",
        "phone",
        "razorpay_order_id",
        "razorpay_payment_id",
    )
    #latest order
    ordering=("-created_at",)
    
    #displaying customer name
    @admin.display(description="customer")
    def customer_name(self,obj):
        return obj.name
    
    # payment status badge
    
    @admin.display(description="Payment status")
    def payment_status_badge(self,obj):
        if obj.payment_status=="paid":
              return format_html(
                '<span style="background:#198754; color:white; '
                'padding:4px 9px; border-radius:12px; '
                'font-weight:600;">Paid</span>'
            )
        elif obj.payment_status=="pending":
            return format_html(
                '<span style="background:#ffc107; color:black; '
                'padding:4px 9px; border-radius:12px; '
                'font-weight:600;">Pending</span>'
            )
        elif obj.payment_status == "failed":
            return format_html(
                '<span style="background:#dc3545; color:white; '
                'padding:4px 9px; border-radius:12px; '
                'font-weight:600;">Failed</span>'
            )

        elif obj.payment_status == "refunded":
            return format_html(
                '<span style="background:#6f42c1; color:white; '
                'padding:4px 9px; border-radius:12px; '
                'font-weight:600;">Refunded</span>'
            )

        return obj.payment_status
    
    
    # oder status badge
    @admin.display(description="Order Status")
    def order_status_badge(self, obj):

        if obj.order_status == "pending":
            return format_html(
                '<span style="background:#ffc107; color:black; '
                'padding:4px 9px; border-radius:12px; '
                'font-weight:600;">Pending</span>'
            )

        elif obj.order_status == "confirmed":
            return format_html(
                '<span style="background:#0d6efd; color:white; '
                'padding:4px 9px; border-radius:12px; '
                'font-weight:600;">Confirmed</span>'
            )

        elif obj.order_status == "processing":
            return format_html(
                '<span style="background:#fd7e14; color:white; '
                'padding:4px 9px; border-radius:12px; '
                'font-weight:600;">Processing</span>'
            )

        elif obj.order_status == "shipped":
            return format_html(
                '<span style="background:#6f42c1; color:white; '
                'padding:4px 9px; border-radius:12px; '
                'font-weight:600;">Shipped</span>'
            )

        elif obj.order_status == "delivered":
            return format_html(
                '<span style="background:#198754; color:white; '
                'padding:4px 9px; border-radius:12px; '
                'font-weight:600;">Delivered</span>'
            )

        elif obj.order_status == "cancelled":
            return format_html(
                '<span style="background:#dc3545; color:white; '
                'padding:4px 9px; border-radius:12px; '
                'font-weight:600;">Cancelled</span>'
            )

        return obj.order_status

        
        
admin.site.register(OrderItem)


