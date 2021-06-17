import pytest
from rest_framework.renderers import JSONRenderer
from django.contrib.auth.models import User, Group, Permission
from django.conf import settings
from products.models import Product, ProductStock
from products.serializers import ProductDataSerializer, ProductSerializer

# Product Fixtures


def create_product_object(id):
    return Product(name=f'Test-Product-{id}', code=f'TP-{id}', price=id, unit='item')


def create_product_stock_object(id):
    return ProductStock(product_id=id, stock_size=id*50)


@pytest.fixture(scope='class')
def product_object(request):
    p = create_product_object(1)
    request.cls.product_object = p
    product_serializer = ProductDataSerializer(p)
    product_object_data = product_serializer.data
    request.cls.product_data = product_object_data


@pytest.fixture(scope='class')
def three_products_db(request):
    n = 3
    for i in range(2, 2+n):
        p = create_product_object(i+1)
        p.save()

    products = Product.objects.all()
    product_serializer = ProductSerializer(products, many=True)
    request.cls.products_json = JSONRenderer().render(product_serializer.data)









