from rest_framework import serializers

from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    itemName = serializers.CharField(source='item_name')
    itemPrice = serializers.IntegerField(source='item_price')
    stockQuantity = serializers.IntegerField(source='stock_quantity')

    class Meta:
        model = Item
        fields = ['id', 'itemName', 'itemPrice', 'stockQuantity']