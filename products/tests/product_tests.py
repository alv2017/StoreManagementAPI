import pytest
import json
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from products.models import Product
from products.serializers import ProductSerializer
from products.views import ProductListView, ProductDetailView


@pytest.mark.usefixtures("db",
                         "three_products_db", "product_object",
                         "regular_user", "member_of_staff", "store_administrator")
class ProductListViewTest(APITestCase):
    view = ProductListView
    url = reverse(view.name)
    factory = APIRequestFactory()

    def test_anonymous_cant_view_products_list(self):
        view = self.view.as_view()

        request = self.factory.get(self.url)
        response = view(request)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_cant_create_product(self):
        view = self.view.as_view()

        request = self.factory.post(self.url, self.product_data)
        response = view(request)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_regular_user_cant_view_products_list(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_regular_user_cant_create_product(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        request = self.factory.post(self.url, self.product_data)
        force_authenticate(request, user=auth_user)
        response = view(request)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_staff_can_view_products_list(self):
        view = self.view.as_view()
        request = self.factory.get(self.url)

        auth_user = self.member_of_staff
        force_authenticate(request, user=auth_user)
        response = view(request)
        response.render()

        # Response Content
        assert response.content == self.products_json
        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

    def test_staff_can_create_product(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        # Number of products before request
        number_of_products_before_request = Product.objects.count()

        request = self.factory.post(self.url, self.product_data)
        force_authenticate(request, user=auth_user)
        response = view(request)
        response.render()

        # Number of Products before and after Request
        number_of_products_after_request = Product.objects.count()
        assert number_of_products_after_request == number_of_products_before_request + 1

        # Response Content
        created_product = Product.objects.get(code=self.product_object.code)
        created_product_serializer = ProductSerializer(created_product)
        created_product_json = JSONRenderer().render(created_product_serializer.data)
        assert created_product_json == response.content
        # Response Status Code
        assert response.status_code == status.HTTP_201_CREATED

    def test_store_administrator_can_view_products_list(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request)
        response.render()

        # Response Content
        assert response.content == self.products_json
        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

    def test_store_administrator_can_create_product(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        # Number of products before request
        number_of_products_before_request = Product.objects.count()

        request = self.factory.post(self.url, self.product_data)
        force_authenticate(request, user=auth_user)
        response = view(request)
        response.render()

        # Number of Products before and after Request
        number_of_products_after_request = Product.objects.count()
        assert number_of_products_after_request == number_of_products_before_request + 1

        # Response Content
        created_product = Product.objects.get(code=self.product_object.code)
        created_product_serializer = ProductSerializer(created_product)
        created_product_json = JSONRenderer().render(created_product_serializer.data)
        assert created_product_json == response.content

        # Response Status Code
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.usefixtures("db",
                         "three_products_db",
                         "regular_user", "member_of_staff", "store_administrator")
class ProductDetailViewTest(APITestCase):
    view = ProductDetailView
    product_pk = 1
    url = reverse(view.name, kwargs={'pk': str(product_pk)})
    factory = APIRequestFactory()

    def test_anonymous_cant_view_product_details(self):
        view = self.view.as_view()

        request = self.factory.get(self.url)
        response = view(request, pk=self.product_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_cant_update_product_details(self):
        view = self.view.as_view()

        product = Product.objects.get(pk=self.product_pk)
        initial_price = product.price
        new_price = product.price + 2
        product.price = new_price
        product_serializer = ProductSerializer(product)
        product_data = product_serializer.data

        request = self.factory.put(self.url, product_data)
        response = view(request, pk=self.product_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_cant_patch_product_detaisl(self):
        view = self.view.as_view()

        product = Product.objects.get(pk=self.product_pk)
        initial_price = product.price
        new_price = product.price + 2
        product.price = new_price
        patch_data = {"price": str(new_price)}

        request = self.factory.patch(self.url, patch_data)
        response = view(request, pk=self.product_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_cant_delete_product(self):
        view = self.view.as_view()

        product = Product.objects.get(pk=self.product_pk)
        assert product.pk == 1

        request = self.factory.delete(self.url)
        response = view(request, pk=self.product_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_regular_user_cant_view_product_details(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.product_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_regular_user_cant_update_product_details(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        product = Product.objects.get(pk=self.product_pk)
        initial_price = product.price
        new_price = product.price + 2
        product.price = new_price
        product_serializer = ProductSerializer(product)
        product_data = product_serializer.data

        request = self.factory.put(self.url, product_data)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.product_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_regular_user_cant_patch_product_details(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        product = Product.objects.get(pk=self.product_pk)
        initial_price = product.price
        new_price = product.price + 2
        product.price = new_price
        patch_data = {"price": str(new_price)}

        request = self.factory.patch(self.url, patch_data)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.product_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_regular_user_cant_delete_product(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        product = Product.objects.get(pk=self.product_pk)
        assert product.pk == 1

        request = self.factory.delete(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.product_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_staff_can_view_product_details(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.product_pk)
        response.render()

        # Response Content
        product_with_pk_1 = Product.objects.get(pk=self.product_pk)
        product_serializer = ProductSerializer(product_with_pk_1)
        product_json = JSONRenderer().render(product_serializer.data)
        assert response.content == product_json

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

    def test_staff_can_update_product_details(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        product = Product.objects.get(pk=self.product_pk)
        initial_price = product.price
        new_price = product.price + 2
        product.price = new_price
        product_serializer = ProductSerializer(product)
        product_data = product_serializer.data

        request = self.factory.put(self.url, product_data)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.product_pk)
        response.render()

        # Response Content
        response_data = json.loads(response.content)
        assert initial_price != new_price
        response_data['price'] == new_price

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

    def test_staff_can_patch_product_details(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        product = Product.objects.get(pk=self.product_pk)
        initial_price = product.price
        new_price = product.price + 2
        product.price = new_price
        patch_data = {"price": str(new_price)}

        request = self.factory.patch(self.url, patch_data)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.product_pk)
        response.render()

        # Response Content
        response_data = json.loads(response.content)
        assert initial_price != new_price
        response_data['price'] == new_price

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

    def test_staff_can_delete_product(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        product = Product.objects.get(pk=self.product_pk)
        assert product.pk == 1

        request = self.factory.delete(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.product_pk)
        response.render()

        # Deleted product is no longer in DB
        with pytest.raises(Product.DoesNotExist):
            Product.objects.get(pk=self.product_pk)

        # Response Status Code
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_store_administrator_can_view_product_details(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, pk='1')
        response.render()

        # Response Content
        product_with_pk_1 = Product.objects.get(pk=1)
        product_serializer = ProductSerializer(product_with_pk_1)
        product_json = JSONRenderer().render(product_serializer.data)
        assert response.content == product_json

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

    def test_store_administrator_can_update_product_details(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        product = Product.objects.get(pk=1)
        initial_price = product.price
        new_price = product.price + 2
        product.price = new_price
        product_serializer = ProductSerializer(product)
        product_data = product_serializer.data

        request = self.factory.put(self.url, product_data)
        force_authenticate(request, user=auth_user)
        response = view(request, pk='1')
        response.render()

        # Response Content
        response_data = json.loads(response.content)
        assert initial_price != new_price
        response_data['price'] == new_price

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

    def test_store_administrator_can_patch_product_details(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        product = Product.objects.get(pk=1)
        initial_price = product.price
        new_price = product.price + 2
        product.price = new_price
        patch_data = {"price": str(new_price)}

        request = self.factory.patch(self.url, patch_data)
        force_authenticate(request, user=auth_user)
        response = view(request, pk='1')
        response.render()

        # Response Content
        response_data = json.loads(response.content)
        assert initial_price != new_price
        response_data['price'] == new_price

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

    def test_store_administrator_can_delete_product(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        product = Product.objects.get(pk=self.product_pk)
        assert product.pk == 1

        request = self.factory.delete(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.product_pk)
        response.render()

        # Deleted product is no longer in DB
        with pytest.raises(Product.DoesNotExist):
            Product.objects.get(pk=self.product_pk)

        # Response Status Code
        assert response.status_code == status.HTTP_204_NO_CONTENT
