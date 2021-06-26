from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_non_negative(value):
    if value < 0:
        raise ValidationError(
            _('%(value)s has to be non-negative'),
            params={'value': value},
        )


class Product(models.Model):
    name = models.CharField(max_length=128)
    code = models.CharField(max_length=10, unique=True)
    price = models.DecimalField(max_digits=8, decimal_places=2, validators=[validate_non_negative])
    unit = models.CharField(max_length=12)
    create_timestamp = models.DateTimeField(auto_now_add=True)
    update_timestamp = models.DateTimeField(auto_now=True, verbose_name='Product Update Time')

    class Meta:
        ordering = ('code',)

    def __str__(self):
        return f"{self.code}: {self.name}, {self.price} USD"

    def save(self, *args, **kwargs):
        isNewInstance = self.pk is None
        super().save(*args, **kwargs)
        if isNewInstance:
            ProductStock.objects.create(product=self)

    @property
    def available_stock(self):
        return self.stock.latest('update_timestamp')

    def add_stock(self, stock_size):
        ProductStock.objects.create(product=self, stock_size=stock_size)


class ProductStock(models.Model):
    product = models.ForeignKey(Product, related_name='stock', on_delete=models.CASCADE)
    stock_size = models.DecimalField(max_digits=12, decimal_places=2, default=0, validators=[validate_non_negative])
    update_timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-update_timestamp',)
        unique_together = ['product', 'update_timestamp']

    def __str__(self):
        return f"{self.stock_size} {self.product.unit}(s)"


