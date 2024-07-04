from rest_framework import viewsets

from .models import Member
from .serializers import MemberSerializer

class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    serializer_class = MemberSerializer

"""
**viewsets.ModelViewSet가 제공하는 메소드**
리스트 조회: 데이터 목록을 가져오는 list() 메서드
개별 항목 조회: 특정 항목을 가져오는 retrieve() 메서드
생성: 새로운 항목을 추가하는 create() 메서드
수정: 기존 항목을 수정하는 update() 및 partial_update() 메서드
삭제: 항목을 삭제하는 destroy() 메서드
"""