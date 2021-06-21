from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductDataSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductDataSerializer()

    class Meta:
        model = OrderItem
        fields = (
            'product',
            'quantity',
            'cost'
        )


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id',
                  'first_name', 'last_name',
                  'email',
                  'address', 'postal_code', 'city', 'country',
                  'created', 'updated')


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id',
                  'first_name', 'last_name',
                  'email',
                  'address', 'postal_code', 'city', 'country',
                  'created', 'updated',
                  'items',
                  'total_cost')


