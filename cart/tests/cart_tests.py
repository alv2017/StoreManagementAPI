import pytest
import json
from django.conf import settings
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from cart.cart import Cart
from rest_framework.test import force_authenticate
from products.models import Product
from products.serializers import ProductSerializer
from products.views import ProductListView, ProductDetailView

factory = APIRequestFactory()
client = APIClient()


@pytest.mark.usefixtures("db", "products_db",
                         "empty_cart", "nonempty_cart")
class CartTests(APITestCase):
    def setUp(self):
        self.mock_request = factory.get('/test-store/')
        self.mock_request.session = client.session

    def test_create_new_cart(self):
        """Test: create a new cart
        """
        mock_request = self.mock_request
        # initially cart does not exist, its session id does not exist
        assert settings.CART_SESSION_ID not in mock_request.session
        # new cart initialization
        cart = Cart(self.mock_request)
        # cart object has been created
        assert cart is not None
        assert isinstance(cart, Cart)
        # cart session id has been created
        assert settings.CART_SESSION_ID in mock_request.session
        # newly created cart is empty
        assert len(cart) == 0

    def test_access_existing_empty_cart(self):
        """ Test: access existing empty shopping cart
        """
        mock_request = self.mock_request_with_empty_cart
        # cart session id exists
        assert settings.CART_SESSION_ID in mock_request.session
        # access the existing cart
        cart = Cart(mock_request)
        # cart is empty
        assert len(cart) == 0
        # cart dictionary (cart.cart) and session cart dictionary reference the same object
        assert id(cart.cart) == self.empty_cart_dict_id

    def test_access_existing_nonempty_cart(self):
        """ Test: access existing nonempty shopping cart
        """
        mock_request = self.mock_request_with_nonempty_cart
        # cart session id exists
        assert settings.CART_SESSION_ID in mock_request.session
        # access existing cart
        cart = Cart(mock_request)
        # cart is non empty
        assert len(cart) > 0
        # cart dictionary (cart.cart) and session cart dictionary reference the same object
        assert id(cart.cart) == self.nonempty_cart_dict_id

    def test_add_product(self):
        mock_request = self.mock_request_with_empty_cart
        # create an empty cart
        cart = Cart(mock_request)
        assert len(cart) == 0
        assert cart.cart == {}
        # add product
        pk1 = 1
        add_1 = 1
        product1 = Product.objects.get(pk=pk1)
        cart.add(product1, add_1)
        assert cart.cart == {
            '1': {'quantity': add_1, 'price': str(product1.price)}
        }
        # add one more product of the same kind
        cart.add(product1, add_1)
        assert cart.cart == {
            '1': {'quantity': 2 * add_1, 'price': str(product1.price)}
        }
        # add 3 products of another kind
        pk2 = 2
        add_3 = 3
        product2 = Product.objects.get(pk=pk2)
        cart.add(product2, add_3)
        assert cart.cart == {
            '1': {'quantity': 2 * add_1, 'price': str(product1.price)},
            '2': {'quantity': add_3, 'price': str(product2.price)}
        }
        assert len(cart) == 2 * add_1 + add_3

    def test_subtract_product_quantity(self):
        mock_request = self.mock_request
        cart = Cart(mock_request)
        product = Product.objects.get(pk=1)
        add_quantity = 10
        subtract_quantity = 5
        invalid_subtract_quantity = add_quantity
        # add products to cart
        cart.add(product, add_quantity)
        assert len(cart) == add_quantity
        # if we try to subtract a quantity that is greater than product quantity in the cart nothing happens
        cart.subtract(product, invalid_subtract_quantity)
        assert len(cart) == add_quantity
        # if we subtract a quantity that is less than product quantity in the cart, the requested quantity subtracted
        cart.subtract(product, subtract_quantity)
        assert len(cart) == add_quantity - subtract_quantity

    def test_remove_product_from_cart(self):
        mock_request = self.mock_request
        cart = Cart(mock_request)
        product = Product.objects.get(pk=1)
        add_quantity = 10
        cart.add(product, 10)
        assert len(cart) == 10
        assert cart.cart == {
            '1': {'quantity': add_quantity, 'price': str(product.price)}
        }
        cart.remove(product)
        assert len(cart) == 0
        assert cart.cart == {}

    def test_number_of_products(self):
        mock_request = self.mock_request
        cart = Cart(mock_request)
        product1 = Product.objects.get(pk=1)
        add_quantity = 1
        # add product to cart, quantity=add_quantity
        cart.add(product1, 1)
        assert len(cart) == add_quantity
        # add the same quantity of the product again
        cart.add(product1, 1)
        assert len(cart) == 2 * add_quantity
        # add product of a different kind
        product2 = Product.objects.get(pk=2)
        cart.add(product2, add_quantity)
        assert len(cart) == 3 * add_quantity
        # add product different from product1 and product2
        product3 = Product.objects.get(pk=3)
        cart.add(product3, add_quantity)
        assert len(cart) == 4

    def test_get_total_price(self):
        mock_request = self.mock_request
        cart = Cart(mock_request)
        product1 = Product.objects.get(pk=1)
        product1_price = product1.price
        add_quantity = 1
        # add product to cart, quantity=add_quantity
        cart.add(product1, 1)
        assert cart.get_total_price() == add_quantity * product1_price

        # add second product to cart
        product2 = Product.objects.get(pk=2)
        product2_price = product2.price
        cart.add(product2, add_quantity)
        assert cart.get_total_price() == add_quantity * (product1_price + product2_price)

        # add third product to cart
        product3 = Product.objects.get(pk=3)
        product3_price = product3.price
        cart.add(product3, add_quantity)
        assert cart.get_total_price() == add_quantity * (product1_price + product2_price + product3_price)

    def test_remove_cart_from_session(self):
        mock_request = self.mock_request
        cart = Cart(mock_request)
        # cart session id created
        assert settings.CART_SESSION_ID in mock_request.session
        cart.clear()
        print(cart)
        assert settings.CART_SESSION_ID not in mock_request.session
