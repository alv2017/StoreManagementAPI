import pytest
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from orders.models import OrderStatus
from orders.serializers import OrderStatusSerializer
from orders.views import OrderStatusListCreateView


@pytest.mark.usefixtures("db",
                         "products_db", "orders_db",
                         "regular_user", "member_of_staff", "store_administrator")
class OrderStatusListCreateViewTest(APITestCase):
    view = OrderStatusListCreateView
    order_id = 1
    url = reverse(view.name, kwargs={'order_id': str(order_id)})
    factory = APIRequestFactory()

    def test_anonymous_cant_view_order_status_list(self):
        view = self.view.as_view()

        request = self.factory.get(self.url)
        response = view(request, order_id=self.order_id)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_anonymous_cant_create_new_order_status(self):
        view = self.view.as_view()

        # let's try to update status by adding a new status ACCEPTED
        new_status_data = {
            "order_id": self.order_id,
            "status": OrderStatus.ACCEPTED,
            "comment": "Order Accepted"
        }

        request = self.factory.post(self.url, new_status_data)
        response = view(request, order_id=self.order_id)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_regular_user_cant_view_order_status_list(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, order_id=self.order_id)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_regular_user_cant_create_new_order_status(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        # let's try to update status by adding a new status ACCEPTED
        new_status_data = {
            "order_id": self.order_id,
            "status": OrderStatus.ACCEPTED,
            "comment": "Order Accepted"
        }

        request = self.factory.post(self.url, new_status_data)
        force_authenticate(request, user=auth_user)
        response = view(request, order_id=self.order_id)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_staff_can_view_order_status_list(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, order_id=self.order_id)
        response.render()

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

        # Response Content
        order_status_objects = OrderStatus.objects.filter(order__id=self.order_id)
        order_status_serializer = OrderStatusSerializer(order_status_objects, many=True)
        order_status_json = JSONRenderer().render(order_status_serializer.data)
        assert response.content == order_status_json

    def test_staff_can_create_new_order_status(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        # order status entries before adding a new status
        status_order_entries_before = OrderStatus.objects.filter(order__id=self.order_id)
        assert len(status_order_entries_before) == 1
        current_status = status_order_entries_before.latest('create_timestamp')
        assert current_status.status == OrderStatus.CREATED

        # let's update status by adding a new status ACCEPTED
        new_status_data = {
            "order_id": self.order_id,
            "status": OrderStatus.ACCEPTED,
            "comment": "Order Accepted"
        }

        request = self.factory.post(self.url, new_status_data)
        force_authenticate(request, user=auth_user)
        response = view(request, order_id=self.order_id)
        response.render()

        # Response Code
        assert response.status_code == status.HTTP_201_CREATED

        # Response Content
        status_order_entries_after = OrderStatus.objects.filter(order__id=self.order_id)
        assert len(status_order_entries_after) == 2
        current_status = status_order_entries_before.latest('create_timestamp')
        assert current_status.status == OrderStatus.ACCEPTED

    def test_store_administrator_can_view_order_status_list(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, order_id=self.order_id)
        response.render()

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

        # Response Content
        order_status_objects = OrderStatus.objects.filter(order__id=self.order_id)
        order_status_serializer = OrderStatusSerializer(order_status_objects, many=True)
        order_status_json = JSONRenderer().render(order_status_serializer.data)
        assert response.content == order_status_json

    def test_store_administrator_can_create_new_order_status(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        # order status entries before adding a new status
        status_order_entries_before = OrderStatus.objects.filter(order__id=self.order_id)
        assert len(status_order_entries_before) == 1
        current_status = status_order_entries_before.latest('create_timestamp')
        assert current_status.status == OrderStatus.CREATED

        # let's update status by adding a new status ACCEPTED
        new_status_data = {
            "order_id": self.order_id,
            "status": OrderStatus.ACCEPTED,
            "comment": "Order Accepted"
        }

        request = self.factory.post(self.url, new_status_data)
        force_authenticate(request, user=auth_user)
        response = view(request, order_id=self.order_id)
        response.render()

        # Response Code
        assert response.status_code == status.HTTP_201_CREATED

        # Response Content
        status_order_entries_after = OrderStatus.objects.filter(order__id=self.order_id)
        assert len(status_order_entries_after) == 2
        current_status = status_order_entries_before.latest('create_timestamp')
        assert current_status.status == OrderStatus.ACCEPTED


