from rest_framework import generics
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.generic import TemplateView
from orders.views import OrderListView
from products.views import ProductListView


class ApiRootView(generics.GenericAPIView):
    name = 'api-root'
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):

        return Response({
            'schema': reverse('openapi-schema', request=request),
            'products': reverse(ProductListView.name, request=request),
            'orders': reverse(OrderListView.name, request=request),
        })

class OpenApiSchemaView(TemplateView):
    name = 'openapi-schema'
    template_name = "openapi/swagger-ui.html"
    permission_classes = (AllowAny,)