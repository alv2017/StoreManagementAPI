from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.response import Response
from orders.views import OrderListView
from products.views import ProductListView


class ApiRoot(generics.GenericAPIView):
    name = 'api-root'

    def get(self, request, *args, **kwargs):

        return Response({
            'schema': reverse('openapi-schema', request=request),
            'products': reverse(ProductListView.name, request=request),
            'orders': reverse(OrderListView.name, request=request),
        })