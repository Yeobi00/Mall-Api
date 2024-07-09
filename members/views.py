"""
**viewsets.ModelViewSet가 제공하는 메소드**
리스트 조회: 데이터 목록을 가져오는 list() 메서드
개별 항목 조회: 특정 항목을 가져오는 retrieve() 메서드
생성: 새로운 항목을 추가하는 create() 메서드
수정: 기존 항목을 수정하는 update() 및 partial_update() 메서드
삭제: 항목을 삭제하는 destroy() 메서드
"""

# viewsets는 CRUD 동작을 자동으로 처리하는 데 중점을 둠.
from rest_framework import viewsets,status
from rest_framework.response import Response
from django.http import Http404

from .models import Member
from .serializers import MemberSerializer

# ModelViewSet : 모든 CRUD 동작을 포함하며, 
# list, retrieve, create, update, partial_update, destroy 메서드를 자동으로 처리함.
class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

    def list(self, request):
        queryset = self.get_queryset()

        if not queryset.exists():
            raise Http404("등록된 사용자가 없습니다.")
        
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
            raise Http404("해당 사용자가 없습니다.")
        
        serializer = self.get_serializer(instance)
        return Response(serializer.data)