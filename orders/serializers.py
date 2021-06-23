from rest_framework import serializers
from .models import Order, OrderItem, OrderStatus
from products.serializers import ProductDataSerializer


class OrderStatusField(serializers.CharField):
    def to_representation(self, value):
        return value.get_status_display()


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


class OrderStatusSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    order_id = serializers.IntegerField()
    status = serializers.CharField(max_length=1)
    status_name = serializers.CharField(read_only=True)
    create_timestamp = serializers.DateTimeField()
    comment = serializers.CharField(max_length=255, allow_blank=True)

    def create(self, validated_data):
        return OrderStatus.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance


class OrderStatusDisplaySerializer(serializers.Serializer):
    status_name = serializers.CharField()
    create_timestamp = serializers.DateTimeField(read_only=True)


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    recent_status = OrderStatusField(source='get_recent_status', read_only=True)
    status_updates = OrderStatusDisplaySerializer(source='get_status_updates', many=True)

    class Meta:
        model = Order
        fields = ('id',
                  'first_name', 'last_name',
                  'email',
                  'address', 'postal_code', 'city', 'country',
                  'created', 'updated',
                  'items',
                  'total_cost',
                  'recent_status',
                  'status_updates'
                  )




