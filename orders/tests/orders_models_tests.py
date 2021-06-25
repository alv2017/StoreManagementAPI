import pytest
from django.utils import timezone
from django.db.utils import IntegrityError
from rest_framework.test import APITestCase
from orders.models import Order, OrderItem, OrderStatus
from products.models import Product


@pytest.mark.usefixtures('db', 'products_db')
class OrderModelTest(APITestCase):
    def setUp(self):
        self.order_creation_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'address': '53 Mortimer Road',
            'postal_code': 'N1 5AR',
            'country': 'United Kingdom'
        }

    def test_create_blank_order(self):
        # Initially Order table is empty
        assert Order.objects.count() == 0
        # Initially OrderStatus table is empty
        assert OrderStatus.objects.count() == 0

        new_order = Order.objects.create(
            first_name=self.order_creation_data['first_name'],
            last_name=self.order_creation_data['last_name'],
            email=self.order_creation_data['email'],
            address=self.order_creation_data['address'],
            postal_code=self.order_creation_data['postal_code'],
            country=self.order_creation_data['country']
        )
        # A new order has been created, and the number of orders is 1
        assert Order.objects.count() == 1

        # Our order was saved to DB
        order = Order.objects.filter(
            first_name=self.order_creation_data['first_name'],
            last_name=self.order_creation_data['last_name'],
            email=self.order_creation_data['email'],
            address=self.order_creation_data['address'],
            postal_code=self.order_creation_data['postal_code'],
            country=self.order_creation_data['country']
        )
        assert len(order) == 1

        # While saving a new order to DB an OrderStatus entry gets created
        assert OrderStatus.objects.count() == 1
        # The newly created status references the new order object we just have created
        order_status = OrderStatus.objects.filter(
            order__first_name=self.order_creation_data['first_name'],
            order__last_name=self.order_creation_data['last_name'],
            order__email=self.order_creation_data['email'],
            order__address=self.order_creation_data['address'],
            order__postal_code=self.order_creation_data['postal_code'],
            order__country=self.order_creation_data['country']
        )
        assert len(order_status) == 1
        # When a new order instance is create, a new order status record is created
        assert order_status[0].status == OrderStatus.CREATED

    def test_order_total_cost_method(self):
        total = 0
        # create order
        new_order = Order.objects.create(
            first_name=self.order_creation_data['first_name'],
            last_name=self.order_creation_data['last_name'],
            email=self.order_creation_data['email'],
            address=self.order_creation_data['address'],
            postal_code=self.order_creation_data['postal_code'],
            country=self.order_creation_data['country']
        )
        # add products to the newly created order
        for product in Product.objects.all():
            p = OrderItem.objects.create(order=new_order, product=product, quantity=2)
            total += p.quantity * p.price

        assert new_order.total_cost == total


@pytest.mark.usefixtures('db', 'products_db')
class OrderItemModelTest(APITestCase):
    def setUp(self):
        self.order_creation_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'address': '53 Mortimer Road',
            'postal_code': 'N1 5AR',
            'country': 'United Kingdom'
        }

        self.new_order = Order.objects.create(
            first_name=self.order_creation_data['first_name'],
            last_name=self.order_creation_data['last_name'],
            email=self.order_creation_data['email'],
            address=self.order_creation_data['address'],
            postal_code=self.order_creation_data['postal_code'],
            country=self.order_creation_data['country']
        )

        self.ordered_product = Product.objects.get(pk=1)
        self.ordered_product_price = self.ordered_product.price
        self.ordered_quantity = 5

    def test_order_item(self):
        # initially OrdeItem with set up parameters is not present in DB
        assert OrderItem.objects.filter(order=self.new_order, product=self.ordered_product,
                                        quantity=self.ordered_quantity).count() == 0
        # create a new order item
        new_order_item = OrderItem.objects.create(order=self.new_order, product=self.ordered_product,
                                                  quantity=self.ordered_quantity)
        # a new order item with given set up parameters has been created in DB
        assert OrderItem.objects.filter(order=self.new_order, product=self.ordered_product,
                                        quantity=self.ordered_quantity).count() == 1
        assert new_order_item.cost == self.ordered_product_price * self.ordered_quantity


@pytest.mark.usefixtures('db', 'products_db')
class OrderStatusModelTest(APITestCase):
    def setUp(self):
        self.order_creation_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'address': '53 Mortimer Road',
            'postal_code': 'N1 5AR',
            'country': 'United Kingdom'
        }

        self.new_order = Order.objects.create(
            first_name=self.order_creation_data['first_name'],
            last_name=self.order_creation_data['last_name'],
            email=self.order_creation_data['email'],
            address=self.order_creation_data['address'],
            postal_code=self.order_creation_data['postal_code'],
            country=self.order_creation_data['country']
        )

        self.ordered_product = Product.objects.get(pk=1)
        self.ordered_product_price = self.ordered_product.price
        self.ordered_quantity = 5

    def test_order_status_options(self):
        order = self.new_order
        # the newly created order is automatically assigned 'C' (Created) status
        assert OrderStatus.objects.filter(order=order).count() == 1
        assert OrderStatus.objects.filter(order=order, status=OrderStatus.CREATED).count() == 1

        # let's create a new status entry: ACCEPTED
        OrderStatus.objects.create(order=order, status=OrderStatus.ACCEPTED)
        assert OrderStatus.objects.filter(order=order, status=OrderStatus.ACCEPTED).count() == 1

        # let's create a new status entry: SENT
        OrderStatus.objects.create(order=order, status=OrderStatus.SENT)
        assert OrderStatus.objects.filter(order=order, status=OrderStatus.SENT).count() == 1

        # let's create a new status entry: DELIVERED
        OrderStatus.objects.create(order=order, status=OrderStatus.DELIVERED)
        assert OrderStatus.objects.filter(order=order, status=OrderStatus.DELIVERED).count() == 1

        # let's create a new status entry: CANCELLED
        OrderStatus.objects.create(order=order, status=OrderStatus.CANCELLED)
        assert OrderStatus.objects.filter(order=order, status=OrderStatus.CANCELLED).count() == 1

        # let's create a new status entry: CLOSED
        OrderStatus.objects.create(order=order, status=OrderStatus.CLOSED)
        assert OrderStatus.objects.filter(order=order, status=OrderStatus.CLOSED).count() == 1

    def test_create_duplicate_status(self):
        order = self.new_order
        # the newly created order is automatically assigned 'C' (Created) status
        assert OrderStatus.objects.filter(order=order).count() == 1
        assert OrderStatus.objects.filter(order=order, status=OrderStatus.CREATED).count() == 1
        with pytest.raises(IntegrityError):
            OrderStatus.objects.create(order=order, status=OrderStatus.CREATED)

