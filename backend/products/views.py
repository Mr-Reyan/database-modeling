import json
from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter,OrderingFilter  
from rest_framework.response import Response
from .models import Product
from .serializers import ProductReadSerializer,ProductWriteSerializer
from config.redis import redis_client



class ProductViewSet(ModelViewSet):

    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    search_fields = ['name','description','sku']
    filterset_fields = ['is_featured','category']
    ordering_fields = ['created_at','price']

    def get_serializer_class(self):
        if self.action in ['list','retrieve']:
            return ProductReadSerializer
        return ProductWriteSerializer
    
    def get_queryset(self):
        queryset = Product.objects.filter(
            is_deleted=False,
            is_active=True,
            tenant=self.request.user.tenant
            ).select_related('category').prefetch_related('tags')
        key = self.request.query_params.get("spec_key")
        value = self.request.query_params.get("spec_value")

        if key and value:
            queryset = queryset.filter(
                specifications__contains={key: value}
            )

        return queryset
    def perform_create(self, serializer):
        serializer.save(
            tenant=self.request.user.tenant
        )
        return super().perform_create(serializer)
    def list(self, request, *args, **kwargs):
        cached = redis_client.get(f"products:{request.user.tenant.id}")

        if cached:
            print("JEYA")
            return Response(json.loads(cached))

        queryset = self.filter_queryset(self.get_queryset()) 
        serializer = self.get_serializer(queryset,many=True)

        redis_client.set(
            f"products:{request.user.tenant.id}",
            json.dumps(serializer.data),
            ex=300
        )
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):

        product = self.get_object()

        product.is_deleted = True

        product.save()

        redis_client.delete(f"products:{request.user.tenant.id}")
        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

    def create(self, request, *args, **kwargs):
        redis_client.delete(f"products:{request.user.tenant.id}")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        redis_client.delete(f"products:{request.user.tenant.id}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        redis_client.delete(f"products:{request.user.tenant.id}")
        return super().partial_update(request, *args, **kwargs)


# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzg1NTg4Mzk1LCJpYXQiOjE3ODU1MDE5OTUsImp0aSI6IjI2MTUxODBiNDBhZjQ0Yzk4ZWU0Zjg4YjhmMWY1ZjM0IiwidXNlcl9pZCI6IjEifQ.kKvfimLF08cMNdG6kTmA_WmEgztk0SIZ3RxFBqRCvVs