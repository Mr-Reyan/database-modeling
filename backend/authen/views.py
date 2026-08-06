from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Tenant

# Create your views here.
User = get_user_model()


@api_view(["POST"])
@permission_classes([AllowAny])
def SignupView(request):
    tenant = Tenant.objects.get(id=2)
    try:
        User.objects.create_user(
            username=request.data.get("username"),
            email=request.data.get("email"),
            password=request.data.get("password"),
            tenant=tenant,
        )
    except Exception:
        return Response({"error": "Error creating user"}, status=403)
    return Response({"info": "User created successfully!"}, status=201)
