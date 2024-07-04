from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Address, Member

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['city', 'street', 'zipcode']

class MemberSerializer(serializers.ModelSerializer):
    memberName = serializers.CharField(source='member_name')
    address = AddressSerializer()

    class Meta:
        model = Member
        fields = ['id', 'memberName', 'address']
    
    def create(self, validated_data):
        address_validated_data = validated_data.pop('address')
        address = Address.objects.create(**address_validated_data)
        return Member.objects.create(address=address, **validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('memberName', instance.name)
        if address_validated_data := validated_data.get('address', None):
            serializer = AddressSerializer(instance.address, data=address_validated_data, partial=True)
            serializer.is_valid(raise_exception=True)
            address = serializer.save()
            instance.address = address
        instance.save()
        return instance
