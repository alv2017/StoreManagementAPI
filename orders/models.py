from django.db import models
from django.utils import timezone
from products.models import Product


class Order(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=32)
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return f'Order {self.id}'

    @property
    def number_of_items(self):
        return self.items.count()

    @property
    def total_cost(self):
        if self.items.count() > 0:
            return sum(item.cost for item in self.items.all())

    def get_recent_status(self):
        recent_status = self.statuses.latest('create_timestamp')
        return recent_status

    def get_status_updates(self):
        return self.statuses

    def save(self, *args, **kwargs):
        isNewInstance = self.pk is None
        super().save(*args, **kwargs)
        if isNewInstance:
            OrderStatus.objects.create(order=self, status=OrderStatus.CREATED)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        isNewInstance = self.pk is None
        if isNewInstance:
            self.price = self.product.price
        super().save(*args, **kwargs)

    @property
    def cost(self):
        return self.price * self.quantity


class OrderStatus(models.Model):
    CREATED = 'C'
    ACCEPTED = 'A'
    SENT = 'S'
    DELIVERED = 'D'
    CLOSED = 'L'
    CANCELLED = 'X'

    STATUS_CHOICES = (
        (CREATED, 'Created'),
        (ACCEPTED, 'Accepted'),
        (SENT, 'Sent'),
        (DELIVERED, 'Delivered'),
        (CLOSED, 'Closed'),
        (CANCELLED, 'Cancelled'),
    )

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='statuses')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    create_timestamp = models.DateTimeField(default=timezone.now)
    comment = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('-order_id', '-create_timestamp',)
        verbose_name_plural = 'Order Statuses'
        unique_together = ['order', 'status']

    def __str__(self):
        return self.status

    @property
    def status_name(self):
        return self.get_status_display()

