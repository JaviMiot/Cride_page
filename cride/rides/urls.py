from django.db import router
from django.urls import path, include

# * Django rest framework
from rest_framework.routers import DefaultRouter

# * views
from .views import rides as rides_views

router = DefaultRouter()
router.register(
    r'circles/(?P<slug_name>[a-zA-Z0-9_-]+)/rides',
    rides_views.RidesViewSet,
    basename='ride'
)
urlpatterns = [
    path('', include(router.urls))
]
