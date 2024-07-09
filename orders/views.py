from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.request import Request
from django.http import Http404

from items.models import Item
from members.models import Member
from orders.models import Order, Order_item
from orders.serializers import OrderRequestDTO, OrderSerializer

class OrderViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    # 특정 사용자의 주문 목록을 조회하여 반환
    def list(self, request: Request):
        member_id = request.query_params.get('member_id', None)
        if (member_id):
            try:
                find_member = Member.objects.get(id=member_id)
            except Member.DoesNotExist:
                raise Http404('해당 사용자가 없습니다.')
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
            member = Member.objects.get(id=data['member_id'])
        except Member.DoesNotExist:
            raise ValidationError('해당 사용자가 없습니다.')
        
        order = Order(member=member)
        order_items = []
        items = []
        for order_item_data in data['items']:
            try:
                item = Item.objects.get(id=order_item_data['item_id'])
            except:
                raise ValidationError('해당 상품이 없습니다.')
            
            item.adjust_stock_quantity(order_item_data['count'], save=False)
            items.append(item)
            order_items.append(Order_item(
                    order=order,
                    item=item,
                    count=order_item_data['count']))
            order.save()
        for order_item in order_items:
            order_item.save()
        for item in items:
            item.save()

        serializer = OrderSerializer(order)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            raise Http404('해당 주문이 없습니다.')

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        instance.status = "주문이 취소되었습니다."
        instance.save()

        serializer = OrderSerializer(instance)
        return Response(serializer.data) 
