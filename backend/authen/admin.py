from django.contrib import admin
from .models import *
from orders.models import Order,OrderItem
from products.models import Product,Category,Tag
from carts.models import Cart
# Register your models here.
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Product)
admin.site.register(User)
admin.site.register(Tenant)
admin.site.register(Cart)


