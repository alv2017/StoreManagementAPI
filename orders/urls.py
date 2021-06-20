from django.urls import path
from .views import OrderListView, OrderDetailView

urlpatterns = [
    path('', OrderListView.as_view(), name=OrderListView.name),
    path('<int:pk>/', OrderDetailView.as_view(), name=OrderDetailView.name),
]