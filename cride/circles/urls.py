from django.db import router
from django.urls import path, include

#* Django rest framework
from rest_framework.routers import DefaultRouter

#* views
from .views import circles as circle_views

router = DefaultRouter()
router.register(r'circles',circle_views.CirclesViewSet, basename='circles')

urlpatterns=[
    path('',include(router.urls))
]

