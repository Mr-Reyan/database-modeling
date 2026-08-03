from django.shortcuts import render
from rest_framework.decorators import api_view
from carts.models import Cart
from inventory.models import Inventory
from .models import Order,OrderItem
from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from config.redis import redis_client
# Create your views here.
from .serializers import OrderSerializer


@api_view(['POST'])
def checkout_order(request):
    cart = get_object_or_404(Cart.objects.prefetch_related('items__product'),user=request.user)
    items = cart.items.all()

    if not items.exists():
        return Response({'error':'Cart is Empty'},status=400)


    with transaction.atomic():
        order = Order.objects.create(user=request.user,total_price=0)
        total = 0
        for item in items:
            inventory = get_object_or_404(
                Inventory.objects.select_for_update(),
                product=item.product
            )

            if(inventory.stock < item.quantity):
                return Response(
                    {"error":f"{item.product.name} is out of stock."},
                    status=400
                )
            inventory.stock -= item.quantity
            inventory.save()

            OrderItem.objects.create(
                order=order,
                product = item.product,
                price_at_purchase = item.product.price,
                quantity = item.quantity,
                product_name = item.product.name,
            )
            total += (item.quantity*item.product.price)

        order.total_price = total
        order.save()

        redis_client.zincrby(
            'top_customers',
            float(order.total_price),
            request.user.username
        )



        items.delete()



        return Response({
                "message": "Order created successfully.",
                "order_id": order.id
            },status=201)


@api_view(['GET'])
def top_customers(request):

    top = redis_client.zrevrange('top_customers',0,2,withscores=True)

    leaderboard = [
        {
            "username": username,
            "score": score
        }
        for username, score in top
    ]
    return Response(leaderboard,status=200)


@api_view(['GET'])
def get_orders(request):
    orders = Order.objects.filter(user=request.user)
    serializer = OrderSerializer(orders,many=True)
    return Response(serializer.data,status=200)