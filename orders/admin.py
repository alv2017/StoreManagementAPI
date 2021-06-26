from django.contrib import admin
from .models import Order, OrderItem, OrderStatus


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderStatusInline(admin.TabularInline):
    model = OrderStatus
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'last_name', 'email',
                    'city', 'country',
                    'created', 'updated',)
    list_filter = ('created', 'updated',)
    inlines = (OrderItemInline, OrderStatusInline, )
    ordering = ('-id',)

