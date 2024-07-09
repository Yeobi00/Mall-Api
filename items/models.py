from django.db import models
from rest_framework.exceptions import ValidationError

class Item(models.Model):
    item_name = models.CharField(max_length=50)
    stock_quantity = models.IntegerField(default=0)
    item_price = models.IntegerField(default=0)

    class Meta:
        db_table = 'item'

    # 아이템 판매 시, 재고 수량을 줄이기 위함.
    def adjust_stock_quantity(self, quantity, save=True):
        if self.stock_quantity < quantity:
            raise ValidationError('상품 재고가 부족합니다.') 
        self.stock_quantity -= quantity

        # save가 True일 경우, 재고 수량을 저장함.
        if save:
            self.save()