from rest_framework import serializers

class OrderItemSerializer(serializers.Serializer):
    itemId = serializers.IntegerField(source='item.id')
    itemName = serializers.CharField(source='item.item_name')
    itemPrice = serializers.IntegerField(source='item.item_price')
    orderQuantity = serializers.IntegerField(source='order_quantity')
    orderStatus = serializers.CharField(source='order_status')

class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    memberId = serializers.IntegerField(source='member.id')
    items = OrderItemSerializer(source='orderitem_set', many=True)
    orderedAt = serializers.DateTimeField(source='ordered_at')

# HTTP 요청으로 받은 데이터를 파싱하고 검증하며, 적절한 형태로 변환하여 뷰 또는 모델에 전달하기 위해 필요함.
class OrderItemRequestDTO(serializers.Serializer):
    itemId = serializers.IntegerField()
    orderQuantity = serializers.IntegerField()

class OrderRequestDTO(serializers.Serializer):
    memberId = serializers.IntegerField()
    items = OrderItemRequestDTO(many=True)