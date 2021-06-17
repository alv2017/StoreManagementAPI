from rest_framework import serializers
from .models import Product, ProductStock


def validate_stock_size(stock_size):
    if stock_size < 0:
        raise serializers.ValidationError('Stock  size has to be positive.')


class AvailableStockField(serializers.CharField):
    def to_representation(self, value):
        return value.stock_size


class ProductDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('name',
                  'code',
                  'price',
                  'unit')


class ProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    available_stock = AvailableStockField(read_only=True)

    class Meta:
        model = Product
        fields = ('id',
                  'name',
                  'code',
                  'price',
                  'unit',
                  'available_stock')


class ProductStockSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField()
    stock_size = serializers.DecimalField(max_digits=12, decimal_places=2, validators=[validate_stock_size])
    update_timestamp = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        return ProductStock.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.stock_size = validated_data.get('stock_size', instance.stock_size)
        instance.save()
        return instance


class IncreaseProductStockSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField()
    stock_size = serializers.DecimalField(max_digits=12, decimal_places=2, validators=[validate_stock_size])
    update_timestamp = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        product_id = validated_data.get('product_id')
        stock_add_value = validated_data.get('stock_size')
        current_stock = ProductStock.objects.filter(product_id=product_id).latest('update_timestamp')
        new_stock_size = current_stock.stock_size + stock_add_value
        return ProductStock.objects.create(product_id=product_id, stock_size=new_stock_size)


class DecreaseProductStockSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    product_id = serializers.IntegerField()
    stock_size = serializers.DecimalField(max_digits=12, decimal_places=2, validators=[validate_stock_size])
    update_timestamp = serializers.DateTimeField(read_only=True)

    def create(self, validated_data):
        product_id = validated_data.get('product_id')
        stock_remove_value = validated_data.get('stock_size')
        current_stock = ProductStock.objects.filter(product_id=product_id).latest('update_timestamp')
        new_stock_size = current_stock.stock_size - stock_remove_value
        print(new_stock_size)
        if new_stock_size >= 0:
            return ProductStock.objects.create(product_id=product_id, stock_size=new_stock_size)
        else:
            raise serializers.ValidationError(f"Not enough products in stock. Available stock: {current_stock}.")

