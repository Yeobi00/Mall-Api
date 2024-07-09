from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.exceptions import ValidationError

from .models import Address, Member

class AddressSerializer(serializers.ModelSerializer):
    class Meta:     # Meta 클래스는 직렬화 설정을 정의함.
        model = Address
        fields = ['city', 'street', 'zipcode']


class MemberSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Member
        fields = ['id', 'name', 'address']

    def validate_name(self, value):
        if Member.objects.filter(name=value).exists():
            raise DuplicateNameErrorException()
        return value

# 유효성 검사를 통과한 데이터들을 바탕으로 새로운 DB 인스턴스를 생성하고 반환함.
    def create(self, validated_data):
        address_validated_data = validated_data.pop('address')
        address = Address.objects.create(**address_validated_data)
        member = Member.objects.create(address=address, **validated_data)
        return member
    
# 유효성 검사를 통과한 데이터들을 바탕으로 기존의 DB 인스턴스를 수정하고 반환함.    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        address_validated_data = validated_data.get('address', None)
        if not validated_data:
            raise UpdateBadRequestException()
        if (address_validated_data):
            serializer = AddressSerializer(instance.address, data=address_validated_data, partial=True)
            serializer.is_valid(raise_exception=True)
            address = serializer.save()
            instance.address = address

        instance.save()
        return instance

class DuplicateNameErrorException(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = '이미 중복된 이름이 있습니다.'

class  UpdateBadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '잘못된 요청입니다.'