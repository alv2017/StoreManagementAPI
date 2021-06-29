from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from django.views.generic import TemplateView
from .views import ApiRoot


urlpatterns = [
    path('', ApiRoot.as_view(), name='ApiRoot.name'),
    path('schema/', TemplateView.as_view(template_name="openapi/swagger-ui.html"), name='openapi-schema'),
    path('admin/', admin.site.urls),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
] + static(settings.STATIC_URL)
