from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductDataSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductDataSerializer()

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'order_id',
            'product',
            'quantity',
            'cost'
        )


class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name',
                  'email',
                  'address', 'postal_code', 'city', 'country',
                  'created', 'updated')


class OrderDisplaySerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id',
                  'first_name', 'last_name',
                  'email',
                  'address', 'postal_code', 'city', 'country',
                  'created', 'updated',
                  'items',
                  'total_cost',
                  )
