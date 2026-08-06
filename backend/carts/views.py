from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from products.models import Product

from .models import Cart, CartItem
from .serializers import CartSerializer


@api_view(["POST"])
def add_to_cart(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    product_id = request.data.get("product_id")
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
        is_deleted=False,
        tenant=request.user.tenant,
    )

    try:
        quantity = int(request.data.get("quantity", 1))
    except (TypeError, ValueError):
        return Response(
            {"error": "Quantity must be an integer"}, status=status.HTTP_400_BAD_REQUEST
        )

    if quantity <= 0:
        return Response(
            {"error": "Quantity must be greater than 0"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    carItem, created = CartItem.objects.get_or_create(
        product=product, cart=cart, defaults={"quantity": quantity}
    )
    if not created:
        carItem.quantity += quantity
        carItem.save()

    return Response({"info": "Product added to cart"}, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def get_cart(request):
    cart = Cart.objects.prefetch_related("items__product").get(user=request.user)
    serializer = CartSerializer(cart)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
def update_cart_quantity(request, product_id):
    product = get_object_or_404(
        Product, id=product_id, is_active=True, is_deleted=False
    )

    try:
        quantity = int(request.data.get("quantity", 1))
    except (TypeError, ValueError):
        return Response(
            {"error": "Quantity must be an integer"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if quantity <= 0:
        return Response(
            {"error": "Quantity must be greater than 0"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    cart = Cart.objects.get(user=request.user)
    cartItem = CartItem.objects.get(cart=cart, product=product)
    cartItem.quantity = quantity
    cartItem.save()
    return Response({"info": "Quantity updated!"}, status=status.HTTP_200_OK)


@api_view(["DELETE"])
def remove_cart_item(request, product_id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(
        Product, id=product_id, is_active=True, is_deleted=False
    )

    cartItem = CartItem.objects.get(cart=cart, product=product)
    cartItem.delete()
    return Response({"info": "Item removed!"}, status=status.HTTP_200_OK)
