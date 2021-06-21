from django.contrib import admin
from .models import Order, OrderItem, OrderStatus


class OrderItemInline(admin.TabularInline):
    model = OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email',
                    'city', 'country',
                    'created', 'updated',)
    list_filter = ('created', 'updated',)
    inlines = (OrderItemInline, )
    ordering = ('-id',)


@admin.register(OrderStatus)
class OrderStatus(admin.ModelAdmin):
    list_display = ['order_id', 'status', 'create_timestamp']
    list_filter = ['status']
    ordering = ['-order_id', '-create_timestamp']

