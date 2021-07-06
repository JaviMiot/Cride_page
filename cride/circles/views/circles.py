
# * Circles views

# * django rest
from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from cride.circles.models import Circle

from cride.circles.serializers import CircleModelSerializer

from cride.circles.models import Membership

from cride.circles.permissions import isCircleAdmin

# *filters
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
#! en este caso hereda excepto el destroy


class CirclesViewSet(mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    """circle view set

    Args:
        viewsets ([type]): [description]
    """

    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'  # * la url cambia y se llama por el slug name

    # *filters
    filter_backends = [SearchFilter, OrderingFilter,DjangoFilterBackend]
    search_fields = ['slug_name', 'name']
    ordering_fields = ['rides_offered', 'rides_taken',
                       'name', 'created', 'member_limit']

    # * cambiar orden por defauld
    ordering = ['-members__count', '-rides_offered', '-rides_taken']

    filter_fields = ['verified', 'is_limited']

    def get_queryset(self):
        """rtestick publict only"""

        queryset = Circle.objects.all()

        if self.action == 'list':
            return queryset.filter(is_public=True)

        return queryset

    def get_permissions(self):
        """Assign permissions based on actions
        """
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(isCircleAdmin)

        return [permission() for permission in permissions]

    def perform_create(self, serializer):
        """Assign circle admin

        Args:
            serializer ([type]): [description]
        """

        circle = serializer.save()
        user = self.request.user
        profile = user.profiles
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_inv=10
        )
