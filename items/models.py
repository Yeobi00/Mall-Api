from django.db import models

from rest_framework.exceptions import ValidationError

class Item(models.Model):
    item_name = models.CharField(max_length=50)
    item_price = models.IntegerField()
    stock_quantity = models.IntegerField()

    # 아이템 판매 시, 재고 수량을 줄이기 위함.
    def sub_stock(self, quantity, save=True):
        if self.stock_quantity - quantity < 0:
            raise ValidationError('재고 부족으로 주문이 불가능합니다.')
        self.stock_quantity -= quantity

        # save 매개변수가 True일 경우, 재고 수량을 저장함.
        if save:
            self.save()