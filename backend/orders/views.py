import json
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from carts.models import Cart
from config.redis_client import redis_client
from inventory.models import Inventory

from .models import Order, OrderItem

# Create your views here.
from .serializers import OrderSerializer


@api_view(["POST"])
def checkout_order(request):
    cart = get_object_or_404(
        Cart.objects.prefetch_related("items__product"), user=request.user
    )
    items = cart.items.all()

    if not items.exists():
        return Response({"error": "Your cart is empty."}, status=400)

    with transaction.atomic():
        order = Order.objects.create(user=request.user, total_price=0)
        total = 0
        for item in items:
            inventory = get_object_or_404(
                Inventory.objects.select_for_update(), product=item.product
            )

            # Check overall inventory stock
            if inventory.stock < item.quantity:
                return Response(
                    {"error": f"{item.product.name} is out of stock."}, status=400
                )

            # Check and deduct specific size stock if available
            if item.product.specifications and "size_stock" in item.product.specifications:
                specs = dict(item.product.specifications)
                size_stock = dict(specs.get("size_stock", {}))
                if item.size and item.size in size_stock:
                    if size_stock[item.size] < item.quantity:
                        return Response(
                            {"error": f"{item.product.name} (Size: {item.size}) has only {size_stock[item.size]} left in stock."},
                            status=400,
                        )
                    size_stock[item.size] -= item.quantity
                    specs["size_stock"] = size_stock
                    item.product.specifications = specs
                    item.product.save(update_fields=["specifications"])

            inventory.stock -= item.quantity
            inventory.save()

            OrderItem.objects.create(
                order=order,
                product=item.product,
                price_at_purchase=item.product.price,
                quantity=item.quantity,
                product_name=item.product.name,
                color=item.color,
                size=item.size
            )
            total += item.quantity * item.product.price

        order.total_price = total
        order.save()

        try:
            redis_client.zincrby(
                "top_customers", float(order.total_price), request.user.username
            )
            # Clear products cache so updated stock reflects immediately
            tenant_id = getattr(request.user.tenant, "id", "")
            for key in redis_client.scan_iter(match=f"products:{tenant_id}*"):
                redis_client.delete(key)
            # Invalidate user orders cache
            redis_client.delete(f"orders:user:{request.user.id}")
        except Exception:
            pass

        items.delete()

        return Response(
            {"message": "Order placed successfully!", "order_id": order.id, "total_price": float(order.total_price)},
            status=201
        )


@api_view(["GET"])
def top_customers(request):
    try:
        top = redis_client.zrevrange("top_customers", 0, 2, withscores=True)
        leaderboard = [{"username": username, "score": score} for username, score in top]
    except Exception:
        leaderboard = []
    return Response(leaderboard, status=200)


@api_view(["GET"])
def get_orders(request):
    cache_key = f"orders:user:{request.user.id}"
    try:
        cached = redis_client.get(cache_key)
        if cached:
            return Response(json.loads(cached), status=200)
    except Exception:
        pass

    orders = (
        Order.objects.filter(user=request.user)
        .prefetch_related("items__product__images")
        .order_by("-created_at")
    )
    serializer = OrderSerializer(orders, many=True)
    data = serializer.data

    try:
        redis_client.setex(cache_key, 3600, json.dumps(data))
    except Exception:
        pass

    return Response(data, status=200)
