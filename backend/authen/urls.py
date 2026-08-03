from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.urls import path
from .views import SignupView
urlpatterns = [
    path('signup/',SignupView),
    path('login/',TokenObtainPairView.as_view()),
    path('token/refresh/',TokenRefreshView.as_view())
]

