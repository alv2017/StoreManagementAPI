import pytest
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from products.models import Product, ProductStock
from products.serializers import ProductStockSerializer
from products.views import ProductStockView, ProductAddStockView, ProductReduceStockView

@pytest.mark.usefixtures("db",
                         "three_products_db",
                         "regular_user", "member_of_staff", "store_administrator")
class ProductStockViewTest(APITestCase):
    view = ProductStockView
    product_id = 1
    url = reverse(view.name, kwargs={'product_id': str(product_id)})
    factory = APIRequestFactory()

    def product_stock_data(self, stock_size):
        return {
            "stock_size": str(stock_size)
        }

    def test_anonymous_cant_view_product_stock(self):
        view = self.view.as_view()

        request = self.factory.get(self.url)
        response = view(request, product_id=self.product_id)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_cant_create_product_stock_entry(self):
        view = self.view.as_view()

        new_stock_size = 100
        stock_data = self.product_stock_data(new_stock_size)

        # Stock entries before request
        product_stock_entries_before_request = ProductStock.objects.filter(product__id=self.product_id).count()

        request = self.factory.post(self.url, stock_data)
        response = view(request, product_id=self.product_id)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_regular_user_cant_view_product_stock(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, product_id=self.product_id)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_regular_user_cant_create_product_stock_entry(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        new_stock_size = 100
        stock_data = self.product_stock_data(new_stock_size)

        # Stock entries before request
        product_stock_entries_before_request = ProductStock.objects.filter(product__id=self.product_id).count()

        request = self.factory.post(self.url, stock_data)
        force_authenticate(request, user=auth_user)
        response = view(request, product_id=self.product_id)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_staff_can_view_product_stock(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, product_id=self.product_id)
        response.render()

        # Response Content
        product_stock = ProductStock.objects.filter(product__id=self.product_id).latest('update_timestamp')
        product_stock_serializer = ProductStockSerializer(product_stock)
        product_stock_json = JSONRenderer().render(product_stock_serializer.data)
        assert response.content == product_stock_json

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

    def test_staff_can_create_product_stock_entry(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        new_stock_size = 100
        stock_data = self.product_stock_data(new_stock_size)

        # Stock entries before request
        product_stock_entries_before_request = ProductStock.objects.filter(product__id=self.product_id).count()

        request = self.factory.post(self.url, stock_data)
        force_authenticate(request, user=auth_user)
        response = view(request, product_id=self.product_id)
        response.render()

        # Stock entries before and after request
        product_stock_entries_after_request = ProductStock.objects.filter(product__id=self.product_id).count()
        assert product_stock_entries_after_request == product_stock_entries_before_request + 1

        # Response Status Code
        assert response.status_code == status.HTTP_201_CREATED

    def test_store_administrator_can_view_product_stock(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, product_id=self.product_id)
        response.render()

        # Response Content
        product_stock = ProductStock.objects.filter(product__id=self.product_id).latest('update_timestamp')
        product_stock_serializer = ProductStockSerializer(product_stock)
        product_stock_json = JSONRenderer().render(product_stock_serializer.data)
        assert response.content == product_stock_json

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

    def test_store_administrator_can_create_product_stock_entry(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        new_stock_size = 100
        stock_data = self.product_stock_data(new_stock_size)

        # Stock entries before request
        product_stock_entries_before_request = ProductStock.objects.filter(product__id=self.product_id).count()

        request = self.factory.post(self.url, stock_data)
        force_authenticate(request, user=auth_user)
        response = view(request, product_id=self.product_id)
        response.render()

        # Stock entries before and after request
        product_stock_entries_after_request = ProductStock.objects.filter(product__id=self.product_id).count()
        assert product_stock_entries_after_request == product_stock_entries_before_request + 1

        # Response Status Code
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.usefixtures("db",
                         "three_products_db",
                         "regular_user", "member_of_staff", "store_administrator")
class ProductAddStockViewTest(APITestCase):
    view = ProductAddStockView
    product_id = 1
    url = reverse(view.name, kwargs={'product_id': str(product_id)})
    factory = APIRequestFactory()

    def product_stock_data(self, stock_size):
        return {
            "stock_size": str(stock_size)
        }

    def test_anonymous_cant_create_add_stock_entry(self):
        view = self.view.as_view()

        add_stock = 50
        stock_data = self.product_stock_data(add_stock)

        # POST Request
        request = self.factory.post(self.url, stock_data)
        response = view(request, product_id=self.product_id)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_regular_user_cant_create_add_stock_entry(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        add_stock = 50
        stock_data = self.product_stock_data(add_stock)

        # POST Request
        request = self.factory.post(self.url, stock_data)
        force_authenticate(request, user=auth_user)
        response = view(request, product_id=self.product_id)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_staff_can_create_add_stock_entry(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        add_stock_1 = 50
        add_stock_2 = 25
        stock_data_1 = self.product_stock_data(add_stock_1)
        stock_data_2 = self.product_stock_data(add_stock_2)

        # Stock entries before request
        product_stock_entries_before_request = ProductStock.objects.filter(product__id=self.product_id).count()

        # Request 1
        request_1 = self.factory.post(self.url, stock_data_1)
        force_authenticate(request_1, user=auth_user)
        response_1 = view(request_1, product_id=self.product_id)
        response_1.render()
        assert response_1.status_code == status.HTTP_201_CREATED

        # Request 2
        request_2 = self.factory.post(self.url, stock_data_2)
        force_authenticate(request_2, user=auth_user)
        response_2 = view(request_2, product_id=self.product_id)
        response_2.render()
        assert response_2.status_code == status.HTTP_201_CREATED

        # Stock entries before and after request
        product_stock_entries_after_request = ProductStock.objects.filter(product__id=self.product_id).count()
        assert product_stock_entries_after_request == product_stock_entries_before_request + 2

        # Latest stock size entry
        latest_stock_size = ProductStock.objects.filter(product__id=self.product_id).latest('update_timestamp')
        assert latest_stock_size.stock_size == add_stock_1 + add_stock_2

    def test_store_administrator_can_create_add_stock_entry(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        add_stock_1 = 50
        add_stock_2 = 25
        stock_data_1 = self.product_stock_data(add_stock_1)
        stock_data_2 = self.product_stock_data(add_stock_2)

        # Stock entries before request
        product_stock_entries_before_request = ProductStock.objects.filter(product__id=self.product_id).count()

        # Request 1
        request_1 = self.factory.post(self.url, stock_data_1)
        force_authenticate(request_1, user=auth_user)
        response_1 = view(request_1, product_id=self.product_id)
        response_1.render()
        assert response_1.status_code == status.HTTP_201_CREATED

        # Request 2
        request_2 = self.factory.post(self.url, stock_data_2)
        force_authenticate(request_2, user=auth_user)
        response_2 = view(request_2, product_id=self.product_id)
        response_2.render()
        assert response_2.status_code == status.HTTP_201_CREATED

        # Stock entries before and after request
        product_stock_entries_after_request = ProductStock.objects.filter(product__id=self.product_id).count()
        assert product_stock_entries_after_request == product_stock_entries_before_request + 2

        # Latest stock size entry
        latest_stock_size = ProductStock.objects.filter(product__id=self.product_id).latest('update_timestamp')
        assert latest_stock_size.stock_size == add_stock_1 + add_stock_2


@pytest.mark.usefixtures("db",
                         "three_products_db",
                         "regular_user", "member_of_staff", "store_administrator")
class ProductReduceStockViewTest(APITestCase):
    view = ProductReduceStockView
    product_id = 1
    url = reverse(view.name, kwargs={'product_id': str(product_id)})
    factory = APIRequestFactory()

    def product_stock_data(self, stock_size):
        return {
            "stock_size": str(stock_size)
        }

    def test_anonymous_cant_create_reduce_stock_entry(self):
        view = self.view.as_view()

        reduce_stock = 50
        stock_data = self.product_stock_data(reduce_stock)

        # POST Request
        request = self.factory.post(self.url, stock_data)
        response = view(request, product_id=self.product_id)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_regular_user_cant_create_reduce_stock_entry(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        reduce_stock = 50
        stock_data = self.product_stock_data(reduce_stock)

        # POST Request
        request = self.factory.post(self.url, stock_data)
        force_authenticate(request, user=auth_user)
        response = view(request, product_id=self.product_id)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_staff_can_create_reduce_stock_entry(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        # Current product stock size is equal to
        product_stock = ProductStock.objects.filter(product__id=self.product_id).latest('update_timestamp')
        assert product_stock.stock_size == 0

        # Lets update stock size to some positive value: 200
        updated_stock_size = 200
        product_stock.stock_size = updated_stock_size
        product_stock.save()

        reduce_stock_size = 50
        stock_data = self.product_stock_data(reduce_stock_size)

        # Stock entries before request
        product_stock_entries_before_request = ProductStock.objects.filter(product__id=self.product_id).count()

        # POST Request (stock reduce request)
        request = self.factory.post(self.url, stock_data)
        force_authenticate(request, user=auth_user)
        response = view(request, product_id=self.product_id)
        response.render()
        assert response.status_code == status.HTTP_201_CREATED

        # Stock entries before and after request
        product_stock_entries_after_request = ProductStock.objects.filter(product__id=self.product_id).count()
        assert product_stock_entries_after_request == product_stock_entries_before_request + 1

        # Latest stock size entry
        latest_stock_size = ProductStock.objects.filter(product__id=self.product_id).latest('update_timestamp')
        assert latest_stock_size.stock_size == updated_stock_size - reduce_stock_size

    def test_store_administrator_can_create_reduce_stock_entry(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        # Current product stock size is equal to
        product_stock = ProductStock.objects.filter(product__id=self.product_id).latest('update_timestamp')
        assert product_stock.stock_size == 0

        # Lets update stock size to some positive value: 200
        updated_stock_size = 200
        product_stock.stock_size = updated_stock_size
        product_stock.save()

        reduce_stock_size = 50
        stock_data = self.product_stock_data(reduce_stock_size)

        # Stock entries before request
        product_stock_entries_before_request = ProductStock.objects.filter(product__id=self.product_id).count()

        # POST Request (stock reduce request)
        request = self.factory.post(self.url, stock_data)
        force_authenticate(request, user=auth_user)
        response = view(request, product_id=self.product_id)
        response.render()
        assert response.status_code == status.HTTP_201_CREATED

        # Stock entries before and after request
        product_stock_entries_after_request = ProductStock.objects.filter(product__id=self.product_id).count()
        assert product_stock_entries_after_request == product_stock_entries_before_request + 1

        # Latest stock size entry
        latest_stock_size = ProductStock.objects.filter(product__id=self.product_id).latest('update_timestamp')
        assert latest_stock_size.stock_size == updated_stock_size - reduce_stock_size

    def test_stock_cant_be_reduced_to_negative_value(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        # Current product stock size is equal to
        product_stock = ProductStock.objects.filter(product__id=self.product_id).latest('update_timestamp')
        assert product_stock.stock_size == 0

        reduce_stock_size = 50
        stock_data = self.product_stock_data(reduce_stock_size)

        # Stock entries before request
        product_stock_entries_before_request = ProductStock.objects.filter(product__id=self.product_id).count()

        # POST Request (stock reduce request)
        request = self.factory.post(self.url, stock_data)
        force_authenticate(request, user=auth_user)
        response = view(request, product_id=self.product_id)
        response.render()
        assert response.content == b'["Not enough products in stock. Available stock: 0.00 item(s)."]'

        # Stock entries before and after request
        product_stock_entries_after_request = ProductStock.objects.filter(product__id=self.product_id).count()
        assert product_stock_entries_after_request == product_stock_entries_before_request

        # Response Status Code
        assert response.status_code == status.HTTP_400_BAD_REQUEST

