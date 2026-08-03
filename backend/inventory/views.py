from .models import Inventory

from .serializers import InventorySerializer
from rest_framework.viewsets import ModelViewSet


class InventoryViewSet(ModelViewSet):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    def get_queryset(self):
        return Inventory.objects.select_related(
            "product"
        )