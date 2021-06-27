import pytest
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from orders.models import Order
from orders.serializers import OrderSerializer
from orders.views import OrderListView

@pytest.mark.usefixtures("db",
                         "products_db", "orders_db",
                         "regular_user", "member_of_staff", "store_administrator")
class OrderListViewTest(APITestCase):
    view = OrderListView
    url = reverse(view.name)
    factory = APIRequestFactory()

    def test_anonymous_cant_view_orders(self):
        view = self.view.as_view()
        request = self.factory.get(self.url)
        response = view(request)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_regular_user_cant_view_orders(self):
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

    def test_staff_can_view_orders(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request)
        response.render()

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

        # Response Content
        order_objects = Order.objects.all()
        orders_serializer = OrderSerializer(order_objects, many=True)
        orders_json = JSONRenderer().render(orders_serializer.data)
        assert response.content == orders_json

    def test_store_administrator_can_view_orders(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request)
        response.render()

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

        # Response Content
        order_objects = Order.objects.all()
        orders_serializer = OrderSerializer(order_objects, many=True)
        orders_json = JSONRenderer().render(orders_serializer.data)
        assert response.content == orders_json



