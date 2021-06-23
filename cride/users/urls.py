from django.urls import path
from cride.users.views import (
    UserLoginAPIView,
    UserSignupAPIView,
    AccountVerifyAPIView
)

urlpatterns = [
    path('users/login/', UserLoginAPIView.as_view(), name='login'),
    path('users/signup/', UserSignupAPIView.as_view(), name='signup'),
    path('users/verify/', AccountVerifyAPIView.as_view(), name='verify')
]
