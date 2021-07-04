from django.utils import timezone
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderStatus
from .serializers import OrderSerializer, OrderDetailSerializer
from .serializers import OrderStatusSerializer, OrderStatusDisplaySerializer
from .permissions import HasGroupPermission
from .filters import OrderFilter


required_groups = {
        'GET': ('store_administrators',),
        'HEAD': ('store_administrators',),
        'OPTIONS': ('store_administrators',),
        'POST': ('store_administrators',),
        'PUT': ('store_administrators',),
        'PATCH': ('store_administrators',),
        'DELETE': ('store_administrators',),
    }


class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (HasGroupPermission,)
    name = 'orders'

    permission_classes = (HasGroupPermission, )
    required_groups = required_groups

    filter_class = OrderFilter

    search_fields = (
        '^last_name',
        '=country'
    )

    ordering_fields = (
        'last_name',
        'country',
        'created'
    )


class OrderDetailView(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderDetailSerializer
    name = 'order-details'

    permission_classes = (HasGroupPermission, )
    required_groups = required_groups


class OrderStatusListCreateView(APIView):
    name = 'order-status-list'
    permission_classes = (HasGroupPermission, )
    required_groups = required_groups

    def get(self, request, order_id):
        try:
            Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            order_status_objects = OrderStatus.objects.filter(order_id=order_id)
            if len(order_status_objects) == 0:
                return Response("No status updates.")

            order_status_serializer = OrderStatusSerializer(order_status_objects, many=True)
            return Response(order_status_serializer.data)

    def post(self, request, order_id):
        try:
            Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            # if order is closed its status can not be updated
            if OrderStatus.objects.filter(order_id=order_id, status=OrderStatus.CLOSED):
                return Response("Closed order can not obtain a new status",
                                status=status.HTTP_403_FORBIDDEN)
            # if order is cancelled its status can not be updatade
            if OrderStatus.objects.filter(order_id=order_id, status=OrderStatus.CANCELLED):
                return Response("Cancelled order can not obtain a new status",
                                status=status.HTTP_403_FORBIDDEN)

            if 'status' not in request.data:
                return Response("Bad request data", status=status.HTTP_400_BAD_REQUEST)

            if 'comment' not in request.data:
                comment = ''
            else:
                comment = request.data["comment"]

            if 'create_timestamp' not in request.data:
                create_timestamp = timezone.now()
            else:
                create_timestamp = request.data["create_timestamp"]

            data = {
                "order_id": order_id,
                "status": request.data["status"],
                "create_timestamp": create_timestamp,
                "comment": comment,
            }

            order_status_serializer = OrderStatusSerializer(data=data)
            if order_status_serializer.is_valid():
                order_status_serializer.save()
                return Response(order_status_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(order_status_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderStatusRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderStatus.objects.all()
    serializer_class = OrderStatusSerializer
    name = 'order-status'

    permission_classes = (HasGroupPermission, )
    required_groups = required_groups

