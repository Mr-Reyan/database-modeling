from rest_framework import serializers
from .models import Inventory
from products.models import Product
from products.serializers import ProductReadSerializer

class InventoryWriteSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all()
    )

    class Meta:
        model = Inventory
        fields = "__all__"


class InventoryReadSerializer(serializers.ModelSerializer):
    product = ProductReadSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = "__all__"