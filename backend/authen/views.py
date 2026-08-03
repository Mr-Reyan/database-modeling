from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.decorators import api_view
from rest_framework.response import Response
# Create your views here.

@api_view(['POST'])
def SignupView(request):
    
    user = User.objects.create(
        username=request.data.get('username'),
        email=request.data.get('email'),
    )
    user.set_password(request.data.get('password'))

    return Response({'info':'User created successfully!'},status=201)