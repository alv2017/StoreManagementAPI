import pytest
from django.contrib.auth.models import User, Group, Permission
from django.conf import settings
from products.models import Product, ProductStock
from orders.models import Order, OrderItem
from orders.serializers import OrderSerializer

# User Fixtures

@pytest.fixture(scope='class')
def store_administrators_group():
    group_name = settings.STORE_ADMINISTRATORS_GROUP
    group = Group.objects.create(name=group_name)

    return group


@pytest.fixture(scope='class')
def store_administrator(request, store_administrators_group):
    user = User.objects.create(username="store_admin",
                               email="store_admin@example.com",
                               password="test1234",
                               is_active=True,
                               is_staff=False)
    user.groups.add(store_administrators_group)
    user = User.objects.get(username="store_admin")
    request.cls.store_administrator = user


@pytest.fixture(scope='class')
def regular_user(request):
    user = User.objects.create(username="regularuser",
                               email="regularuser@example.com",
                               password="test1234",
                               is_active=True,
                               is_staff=False)
    request.cls.regular_user = user


@pytest.fixture(scope='class')
def member_of_staff(request):
    user = User.objects.create(username="staffuser",
                               email="staffuser@example.com",
                               password="test1234",
                               is_active=True,
                               is_staff=True)
    request.cls.member_of_staff = user


# Products

def create_product_object(id):
    return Product(name=f'Test-Product-{id}', code=f'TP-{id}', price=id, unit='item')


def create_product_stock_object(product_id):
    product = Product.objects.get(pk=product_id)
    return ProductStock(product=product, stock_size=product_id * 50)


@pytest.fixture(scope='class')
def products_db(request):
    n = 3
    for i in range(n):
        p = create_product_object(i + 1)
        p = p.save()
        ps = create_product_stock_object(i + 1)
        ps.save()


# Orders

ORDERS_DATA = [{
                    'first_name': 'John', 'last_name': 'Doe',
                    'email': 'john.doe@example.com',
                    'address': '53 Mortimer Road',
                    'postal_code': 'N1 5AR',
                    'city': 'London',
                    'country': 'United Kingdom'
                },
               {
                   'first_name': 'Lisa', 'last_name': 'Arnold',
                   'email': 'lisa.arnold@example.com',
                   'address': '256 York Road',
                   'postal_code': 'RG1 3TE',
                   'city': 'Reading',
                   'country': 'United Kingdom'
               },
               ]


@pytest.fixture(scope='class')
def orders_db(request, products_db):
    for item in ORDERS_DATA:
        new_order = OrderSerializer(data=item)
        if new_order.is_valid():
            new_order_object = new_order.save()
            # add products to newly created order
            for product in Product.objects.all():
                OrderItem.objects.create(order=new_order_object, product=product, quantity=1, price=product.price)


