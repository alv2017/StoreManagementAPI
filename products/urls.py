from django.views.generic import TemplateView
from django.urls import path
from rest_framework.schemas import get_schema_view
from .views import ProductListView, ProductDetailView
from .views import ProductStockView, ProductAddStockView, ProductReduceStockView


urlpatterns = [
    path('', ProductListView.as_view(), name=ProductListView.name),
    path('<int:pk>/', ProductDetailView.as_view(), name=ProductDetailView.name),
    path('stock/<int:product_id>/', ProductStockView.as_view(), name=ProductStockView.name),
    path('stock/add/<int:product_id>/', ProductAddStockView.as_view(), name=ProductAddStockView.name),
    path('stock/reduce/<int:product_id>/', ProductReduceStockView.as_view(), name=ProductReduceStockView.name),
]
