from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from .models import Product
from .models import ProductStock
from .permissions import HasGroupPermission
from .serializers import ProductSerializer
from .serializers import ProductStockSerializer, IncreaseProductStockSerializer, DecreaseProductStockSerializer


required_groups = {
        'GET': ('store_administrators',),
        'HEAD': ('store_administrators',),
        'OPTIONS': ('store_administrators',),
        'POST': ('store_administrators',),
        'PUT': ('store_administrators',),
        'PATCH': ('store_administrators',),
        'DELETE': ('store_administrators',),
    }


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    name = 'products'

    permission_classes = (HasGroupPermission, )
    required_groups = required_groups


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    name = 'product-details'

    permission_classes = (HasGroupPermission, )
    required_groups = required_groups


class ProductStockView(APIView):
    name = 'product-stock'
    permission_classes = (HasGroupPermission, )
    required_groups = required_groups

    def get(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            print('Product does not exist')
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            current_stock = ProductStock.objects.filter(product__pk=product_id).latest('update_timestamp')
            current_stock_serializer = ProductStockSerializer(current_stock)
            return Response(current_stock_serializer.data)

    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            print('Product does not exist')
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            data = {
                "stock_size": request.data["stock_size"],
                "product_id": product_id
            }

            product_stock_serializer = ProductStockSerializer(data=data)
            if product_stock_serializer.is_valid():
                product_stock_serializer.save()
                return Response(product_stock_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(product_stock_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductAddStockView(APIView):
    name = 'product-stock-add'
    permission_classes = (HasGroupPermission, )
    required_groups = required_groups

    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            if 'stock_size' not in request.data:
                return Response("Bad request data", status=status.HTTP_400_BAD_REQUEST)
            data = {
                "stock_size": request.data["stock_size"],
                "product_id": product_id
            }
            product_stock_serializer = IncreaseProductStockSerializer(data=data)
            if product_stock_serializer.is_valid():
                product_stock_serializer.save()
                return Response(product_stock_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(product_stock_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductReduceStockView(APIView):
    name = 'product-stock-reduce'
    permission_classes = (HasGroupPermission, )
    required_groups = required_groups

    def post(self, request, product_id):
        try:
            product = Product.objects.get(pk=product_id)
        except Product.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            data = {
                "stock_size": request.data["stock_size"],
                "product_id": product_id
            }
            product_stock_serializer = DecreaseProductStockSerializer(data=data)
            if product_stock_serializer.is_valid():
                product_stock_serializer.save()
                return Response(product_stock_serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(product_stock_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

