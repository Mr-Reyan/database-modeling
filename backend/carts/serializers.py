from rest_framework.serializers import ModelSerializer
from .models import Cart,CartItem
from products.serializers import ProductReadSerializer

class CartItemSerializer(ModelSerializer):
    product = ProductReadSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = [
            "id",
            "product",
            "quantity",
            "created_at",
        ]


class CartSerializer(ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = [
            "id",
            "user",
            "items",
            "created_at",
            "updated_at",
            "is_deleted",
        ]