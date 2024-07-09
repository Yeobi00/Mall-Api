from rest_framework import viewsets, status
from rest_framework.response import Response
from django.http import Http404

from .models import Item
from .serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def list(self, request):
        queryset = self.get_queryset()

        if not queryset.exists():
            raise Http404("등록된 상품이 없습니다.")
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_200_OK)
    
    def retrieve(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except:
            raise Http404("해당 상품이 없습니다.")
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)