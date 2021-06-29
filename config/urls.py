from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.permissions import AllowAny
from .views import ApiRootView, OpenApiSchemaView


urlpatterns = [
    path('', ApiRootView.as_view(), name=ApiRootView.name),
    path('schema/', OpenApiSchemaView.as_view(), name=OpenApiSchemaView.name),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.STATIC_URL)
