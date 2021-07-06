from django.db import router
from django.urls import path, include

# * Django rest framework
from rest_framework.routers import DefaultRouter

# * views
from .views import circles as circle_views
from .views import memberships as memberships_views

router = DefaultRouter()
router.register(r'circles', circle_views.CirclesViewSet, basename='circles')
router.register(
    r'circles/(?P<slug_name>[a-zA-Z0-9_-]+)/members',
    memberships_views.MembershipViewSet,
    basename='membership'
)
urlpatterns = [
    path('', include(router.urls))
]
