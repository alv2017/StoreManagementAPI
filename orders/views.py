from rest_framework import generics
from .models import Order
from .serializers import OrderSerializer, OrderDetailSerializer
from .permissions import HasGroupPermission


required_groups = {
        'GET': ('store_administrators',),
        'HEAD': ('store_administrators',),
        'OPTIONS': ('store_administrators',),
    }


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (HasGroupPermission,)
    name = 'orders'

    permission_classes = (HasGroupPermission, )
    required_groups = required_groups


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    name = 'order-details'

    permission_classes = (HasGroupPermission, )
    required_groups = required_groups
