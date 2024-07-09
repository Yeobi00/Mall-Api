from django.db import models

class Address(models.Model):
    city = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    zipcode = models.CharField(max_length=50)
    # 참조하는 객체가 삭제될 때, 이 객체와 연결된 객체도 함께 삭제됨.

    class Meta:
        db_table = 'address'

class Member(models.Model):
    name = models.CharField(max_length=50, default="")
    address = models.OneToOneField(Address, on_delete=models.CASCADE, default="")

    class Meta:
        db_table = 'member'
