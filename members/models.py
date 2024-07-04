from django.db import models

class Address(models.Model):
    city = models.CharField(max_length=512)
    street = models.CharField(max_length=512)
    zipcode = models.CharField(max_length=512)


class Member(models.Model):
    member_name = models.CharField(max_length=512)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)
