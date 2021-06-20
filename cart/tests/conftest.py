import pytest

from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from cart.cart import Cart
from products.models import Product, ProductStock

factory = APIRequestFactory()
client = APIClient()

@pytest.fixture(scope='class')
def products_db(request):
    n = 3
    for id in range(1, n+1):
        p = Product(name=f'Test-Product-{id}', code=f'TP-{id}', price=id, unit='item')
        p.save()
        p.add_stock(stock_size=id*100)


@pytest.fixture(scope='class')
def empty_cart(request):
    mock_request = factory.get('/test-store-empty-cart/')
    mock_request.session = client.session
    cart = Cart(mock_request)
    request.cls.mock_request_with_empty_cart = mock_request
    request.cls.empty_cart_dict_id = id(cart.cart)


@pytest.fixture(scope='class')
def nonempty_cart(request, products_db):
    mock_request = factory.get('/test-store-nonempty-cart/')
    mock_request.session = client.session
    cart = Cart(mock_request)
    product = Product.objects.get(pk=1)
    cart.add(product, 10)
    request.cls.mock_request_with_nonempty_cart = mock_request
    request.cls.nonempty_cart_dict_id = id(cart.cart)



