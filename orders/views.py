from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request

from items.models import Item
from members.models import Member
from orders.models import Order, OrderItem
from orders.serializers import OrderRequestDTO, OrderSerializer

# mixin은 각각 하나의 기능만을 담당하고, 공통된 기능을 여러 클래스에서 재사용하기 위해 사용함.
class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # 특정 사용자의 주문 목록을 조회하여 반환
    def list(self, request: Request):
        if member_id := request.query_params.get('memberId', None):
            orders = Order.objects.filter(member_id=member_id)
        else:
            orders = Order.objects.none()
        
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
    

    def create(self, request):
        # 요청 데이터를 OrderRequestDTO 시리얼라이저를 사용하여 검증함.
        serializer = OrderRequestDTO(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            member = Member.objects.get(id=data['memberId'])
        except Member.DoesNotExist:
            raise ValidationError('memberId를 가지는 사용자가 존재하지 않습니다.')
        
        order = Order(member=member)
        order_items = []
        items = []
        for order_item_data in data['items']:
            try:
                item = Item.objects.get(id=order_item_data['itemId'])
            except:
                raise ValidationError('itemId를 가지는 상품이 존재하지 않습니다.')
            
            item.sub_stock(order_item_data['orderQuantity'], save=False)
            items.append(item)
            order_items.append(OrderItem(
                    order=order,
                    item=item,
                    order_quantity=order_item_data['orderQuantity']))

        order.save()
        for order_item in order_items:
            order_item.save()
        for item in items:
            item.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data)    
