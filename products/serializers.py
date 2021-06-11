from re import I
from django.contrib.auth import models
from django.db.models import fields
from rest_framework import serializers
from .models import Product

class ProductSerializers(serializers.ModelSerializer):

    class Meta:

        model = Product
        fields = "__all__"


