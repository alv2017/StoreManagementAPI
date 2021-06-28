from django.urls import path
from .views import OrderListView, OrderDetailView
from .views import OrderStatusListCreateView
from .views import OrderStatusRetrieveUpdateDeleteView

urlpatterns = [
    path('', OrderListView.as_view(), name=OrderListView.name),
    path('<int:pk>/', OrderDetailView.as_view(), name=OrderDetailView.name),
    path('<int:order_id>/status/', OrderStatusListCreateView.as_view(), name=OrderStatusListCreateView.name),
    path('status/<int:pk>/', OrderStatusRetrieveUpdateDeleteView.as_view(),
         name=OrderStatusRetrieveUpdateDeleteView.name),
]
