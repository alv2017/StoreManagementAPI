from django.views.generic import TemplateView
from django.urls import path
from rest_framework.schemas import get_schema_view
from .views import ProductListView, ProductDetailView
from .views import ProductStockView, ProductAddStockView, ProductReduceStockView


urlpatterns = [
    path('', ProductListView.as_view(), name=ProductListView.name),
    path('<int:pk>/', ProductDetailView.as_view(), name=ProductDetailView.name),
    path('<int:product_id>/stock/', ProductStockView.as_view(), name=ProductStockView.name),
    path('<int:product_id>/stock/add/', ProductAddStockView.as_view(), name=ProductAddStockView.name),
    path('<int:product_id>/stock/reduce/', ProductReduceStockView.as_view(), name=ProductReduceStockView.name),
]
