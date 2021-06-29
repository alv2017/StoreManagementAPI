import pytest
from rest_framework.reverse import reverse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory
from rest_framework.test import force_authenticate
from orders.models import OrderStatus
from orders.serializers import OrderStatusSerializer
from orders.views import OrderStatusRetrieveUpdateDeleteView


@pytest.mark.usefixtures("db",
                         "products_db", "orders_db",
                         "regular_user", "member_of_staff", "store_administrator")
class OrderStatusRetrieveUpdateDeleteViewTest(APITestCase):
    view = OrderStatusRetrieveUpdateDeleteView
    status_pk = 1
    url = reverse(view.name, kwargs={'pk': str(status_pk)})
    factory = APIRequestFactory()

    def test_anonymous_can_not_view_order_status_entries(self):
        view = self.view.as_view()

        request = self.factory.get(self.url)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_regular_user_can_not_view_order_status_entries(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_staff_can_view_order_status_entries(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Content
        order_status = OrderStatus.objects.get(pk=self.status_pk)
        order_status_serializer = OrderStatusSerializer(order_status)
        order_status_json = JSONRenderer().render(order_status_serializer.data)
        assert response.content == order_status_json

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

    def test_store_administrator_can_view_order_status_entries(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        request = self.factory.get(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Content
        order_status = OrderStatus.objects.get(pk=self.status_pk)
        order_status_serializer = OrderStatusSerializer(order_status)
        order_status_json = JSONRenderer().render(order_status_serializer.data)
        assert response.content == order_status_json

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

    def test_anonymous_can_not_update_order_status_entries(self):
        view = self.view.as_view()
        updated_status = OrderStatus.ACCEPTED
        updated_comment = "Order Accepted for Execution"

        order_status = OrderStatus.objects.get(pk=self.status_pk)
        # initial order status
        initial_status = order_status.status
        assert initial_status == 'C'
        # let's change status to accepted
        order_status.status = updated_status
        # initial comment
        initial_comment = order_status.comment
        assert initial_comment is None
        # let's change comment
        order_status.comment = updated_comment

        order_status_serializer = OrderStatusSerializer(order_status)
        request = self.factory.put(self.url, order_status_serializer.data)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_regular_user_can_not_update_order_status_entries(self):
        view = self.view.as_view()
        auth_user = self.regular_user
        updated_status = OrderStatus.ACCEPTED
        updated_comment = "Order Accepted for Execution"

        order_status = OrderStatus.objects.get(pk=self.status_pk)
        # initial order status
        initial_status = order_status.status
        assert initial_status == 'C'
        # let's change status to accepted
        order_status.status = updated_status
        # initial comment
        initial_comment = order_status.comment
        assert initial_comment is None
        # let's change comment
        order_status.comment = updated_comment

        order_status_serializer = OrderStatusSerializer(order_status)
        request = self.factory.put(self.url, order_status_serializer.data)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_staff_can_update_order_status_entries(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff
        updated_status = OrderStatus.ACCEPTED
        updated_comment = "Order Accepted for Execution"

        order_status = OrderStatus.objects.get(pk=self.status_pk)
        # initial order status
        initial_status = order_status.status
        assert initial_status == 'C'
        # let's change status to accepted
        order_status.status = updated_status
        # initial comment
        initial_comment = order_status.comment
        assert initial_comment is None
        # let's change comment
        order_status.comment = updated_comment

        order_status_serializer = OrderStatusSerializer(order_status)
        request = self.factory.put(self.url, order_status_serializer.data)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

        # Order status object has been changed in DB
        updated_status = OrderStatus.objects.get(pk=self.status_pk)
        assert updated_status.status != initial_status
        assert updated_status.status == OrderStatus.ACCEPTED
        assert updated_status.comment != initial_comment
        assert updated_status.comment == updated_comment

    def test_store_administrator_can_update_order_status_entries(self):
        view = self.view.as_view()
        auth_user = self.store_administrator
        updated_status = OrderStatus.ACCEPTED
        updated_comment = "Order Accepted for Execution"

        order_status = OrderStatus.objects.get(pk=self.status_pk)
        # initial order status
        initial_status = order_status.status
        assert initial_status == 'C'
        # let's change status to accepted
        order_status.status = updated_status
        # initial comment
        initial_comment = order_status.comment
        assert initial_comment is None
        # let's change status comment
        updated_comment = updated_comment
        order_status.comment = updated_comment

        order_status_serializer = OrderStatusSerializer(order_status)
        request = self.factory.put(self.url, order_status_serializer.data)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

        # Order status object has been changed in DB
        updated_status = OrderStatus.objects.get(pk=self.status_pk)
        assert updated_status.status != initial_status
        assert updated_status.status == OrderStatus.ACCEPTED
        assert updated_status.comment != initial_comment
        assert updated_status.comment == updated_comment

    def test_anonymous_can_not_patch_order_status_entries(self):
        view = self.view.as_view()
        updated_status = OrderStatus.ACCEPTED
        updated_comment = "Order Accepted for Execution"

        order_status = OrderStatus.objects.get(pk=self.status_pk)
        # initial order status
        initial_status = order_status.status
        assert initial_status == 'C'
        # initial comment
        initial_comment = order_status.comment
        assert initial_comment is None

        # let's patch order status
        patch_data = {
            "status": updated_status,
            "comment": updated_comment
        }

        request = self.factory.patch(self.url, patch_data)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_regular_user_can_not_patch_order_status_entries(self):
        view = self.view.as_view()
        auth_user = self.regular_user
        updated_status = OrderStatus.ACCEPTED
        updated_comment = "Order Accepted for Execution"

        order_status = OrderStatus.objects.get(pk=self.status_pk)
        # initial order status
        initial_status = order_status.status
        assert initial_status == 'C'
        # initial comment
        initial_comment = order_status.comment
        assert initial_comment is None

        # let's patch order status
        patch_data = {
            "status": updated_status,
            "comment": updated_comment
        }

        request = self.factory.patch(self.url, patch_data)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_staff_can_patch_order_status_entries(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff
        updated_status = OrderStatus.ACCEPTED
        updated_comment = "Order Accepted for Execution"

        order_status = OrderStatus.objects.get(pk=self.status_pk)
        # initial order status
        initial_status = order_status.status
        assert initial_status == 'C'
        # initial comment
        initial_comment = order_status.comment
        assert initial_comment is None

        # let's patch order status
        patch_data = {
            "status": updated_status,
            "comment": updated_comment
        }

        request = self.factory.patch(self.url, patch_data)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

        # Order status object has been changed in DB
        updated_status = OrderStatus.objects.get(pk=self.status_pk)
        assert updated_status.status != initial_status
        assert updated_status.status == OrderStatus.ACCEPTED
        assert updated_status.comment != initial_comment
        assert updated_status.comment == updated_comment

    def test_store_administrator_can_patch_order_status_entries(self):
        view = self.view.as_view()
        auth_user = self.store_administrator
        updated_status = OrderStatus.ACCEPTED
        updated_comment = "Order Accepted for Execution"

        order_status = OrderStatus.objects.get(pk=self.status_pk)
        # initial order status
        initial_status = order_status.status
        assert initial_status == 'C'
        # initial comment
        initial_comment = order_status.comment
        assert initial_comment is None

        # let's patch order status
        patch_data = {
            "status": updated_status,
            "comment": updated_comment
        }

        request = self.factory.patch(self.url, patch_data)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Status Code
        assert response.status_code == status.HTTP_200_OK

        # Order status object has been changed in DB
        updated_status = OrderStatus.objects.get(pk=self.status_pk)
        assert updated_status.status != initial_status
        assert updated_status.status == OrderStatus.ACCEPTED
        assert updated_status.comment != initial_comment
        assert updated_status.comment == updated_comment

    def test_anonymous_can_not_delete_order_status_entries(self):
        view = self.view.as_view()

        # before request
        assert OrderStatus.objects.filter(pk=self.status_pk).count() == 1

        request = self.factory.delete(self.url)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"Authentication credentials were not provided."}'
        # Response Status Code
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        # after request
        assert OrderStatus.objects.filter(pk=self.status_pk).count() == 1

    def test_regular_user_can_not_delete_order_status_entries(self):
        view = self.view.as_view()
        auth_user = self.regular_user

        # before request
        assert OrderStatus.objects.filter(pk=self.status_pk).count() == 1

        request = self.factory.delete(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Content
        assert response.content == b'{"detail":"You do not have permission to perform this action."}'
        # Response Status Code
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # after request
        assert OrderStatus.objects.filter(pk=self.status_pk).count() == 1

    def test_staff_can_delete_order_status_entries(self):
        view = self.view.as_view()
        auth_user = self.member_of_staff

        # before request
        assert OrderStatus.objects.filter(pk=self.status_pk).count() == 1

        request = self.factory.delete(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Status Code
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # after request
        assert OrderStatus.objects.filter(pk=self.status_pk).count() == 0

    def test_store_administrator_can_delete_order_status_entries(self):
        view = self.view.as_view()
        auth_user = self.store_administrator

        # before request
        assert OrderStatus.objects.filter(pk=self.status_pk).count() == 1

        request = self.factory.delete(self.url)
        force_authenticate(request, user=auth_user)
        response = view(request, pk=self.status_pk)
        response.render()

        # Response Status Code
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # after request
        assert OrderStatus.objects.filter(pk=self.status_pk).count() == 0
