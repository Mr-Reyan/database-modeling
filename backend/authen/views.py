from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def SignupView(request):
    
    user = User.objects.create(
        username=request.data.get('username'),
        email=request.data.get('email'),
    )
    user.set_password(request.data.get('password'))

    return Response({'info':'User created successfully!'},status=201)