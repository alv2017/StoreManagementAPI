from django.contrib import admin
from .models import Product, ProductStock


class ProductStockInline(admin.TabularInline):
    model = ProductStock
    extra = 1

    def get_queryset(self, request):
        product_id = request.resolver_match.kwargs.get('object_id')
        qs = ProductStock.objects.filter(product__id=product_id)
        latest_stock_update = qs.latest('update_timestamp')
        return qs.filter(pk=latest_stock_update.pk)

    def has_add_permission(self, request, obj):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fields = ('id', 'name', 'code', 'price')
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'code', 'price', 'update_timestamp', 'stock_size', 'stock_update_time')

    inlines = [ProductStockInline]

    @admin.display(description='Stock Size')
    def stock_size(self, obj):
        return obj.available_stock.stock_size

    @admin.display(description='Stock Update Time')
    def stock_update_time(self, obj):
        return obj.available_stock.update_timestamp
