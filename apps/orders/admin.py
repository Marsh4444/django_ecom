from django.contrib import admin

from apps.orders.models import Order, OrderProduct, Payment

# Register your models here.
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'payment_method', 'amount_paid', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('payment_id', 'payment_method', 'amount_paid', 'status')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'first_name', 'last_name', 'phone', 'email', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'order_note', 'order_total', 'tax', 'status', 'ip', 'is_ordered', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_number', 'first_name', 'last_name', 'phone', 'email')

@admin.register(OrderProduct)
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('order', 'payment', 'product', 'user', 'variation', 'color', 'size', 'quantity', 'product_price', 'ordered')
    list_filter = ('ordered',)
    search_fields = ('order__order_number', 'payment__payment_id', 'product__name', 'user__email')