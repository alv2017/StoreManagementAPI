import pytest
from products.models import Product, ProductStock


def create_product_object(id):
    return Product(name=f'Test-Product-{id}', code=f'TP-{id}', price=id, unit='item')


def create_product_stock_object(id):
    return ProductStock(product_id=id, stock_size=id*50)


@pytest.fixture(scope='class')
def products_db(request):
    n = 3
    for i in range(n):
        p = create_product_object(i+1)
        p = p.save()
        ps = create_product_stock_object(i+1)
        ps.save()
