from django.db import models

from items.models import Item
from members.models import Member

class OrderStatus(models.TextChoices):
    IN_PROGRESS = 'IPRG', 'In progress'
    DONE = 'DONE', 'Done'

class Order(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    items = models.ManyToManyField(Item, through='OrderItem')
    ordered_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    order_quantity = models.IntegerField()
    order_status = models.TextField(max_length=50, choices=OrderStatus.choices, default=OrderStatus.IN_PROGRESS)