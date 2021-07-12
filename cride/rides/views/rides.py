

from datetime import timedelta
from rest_framework import mixins, serializers, viewsets, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from cride.circles.permissions import IsActiveCircleMember

from cride.rides.serializers import (CreateRidesSerializer,
                                     RideModelSerializer,
                                     JoinRideSerializer,
                                     EndRideSerializer,)

from cride.circles.models import Circle

from datetime import timedelta
from django.utils import timezone

# * filters
from rest_framework.filters import SearchFilter, OrderingFilter

# * permitions
from cride.rides.permissions import IsRideOwner, IsNotRideOwner, ride

# * actions
from rest_framework.decorators import action


class RidesViewSet(mixins.CreateModelMixin,
                   mixins.ListModelMixin,
                   mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):

    serializer_class = CreateRidesSerializer
    permission_classes = [IsAuthenticated, IsActiveCircleMember]
    filter_backends = [SearchFilter, OrderingFilter]

    filter_backends = (SearchFilter, OrderingFilter)
    ordering = ('departure_date', 'arrival_date', 'available_seats')
    ordering_fields = ('departure_date', 'arrival_date', 'available_seats')
    search_fields = ('departure_location', 'arrival_location')

    def dispatch(self, request, *args, **kwargs):
        slug_name = kwargs['slug_name']
        self.circle = get_object_or_404(
            Circle,
            slug_name=slug_name
        )

        return super(RidesViewSet, self).dispatch(request, *args, **kwargs)

    def get_permissions(self):
        permissions = [IsAuthenticated, IsActiveCircleMember]
        if self.action in ['update', 'partial_update', 'finish']:
            permissions.append(IsRideOwner)
        if self.action == 'join':
            permissions.append(IsNotRideOwner)

        return [p() for p in permissions]

    def get_serializer_context(self):
        context = super(RidesViewSet, self).get_serializer_context()
        context['circle'] = self.circle
        return context

    def get_serializer_class(self):
        """retuirna un serializar basada en un accion"""
        if self.action == 'create':
            return CreateRidesSerializer
        if self.action == 'update':
            return JoinRideSerializer
        if self.action == 'finish':
            return EndRideSerializer
        return RideModelSerializer

    def get_queryset(self):
        """return active circles rides"""
        if self.action != 'finish':
            offset = timezone.now() + timedelta(minutes=10)
            return self.circle.ride_set.filter(
                departure_date__gte=offset,
                is_active=True,
                available_seats__gte=1
            )
        else:
            return self.circle.ride_set.all()

    @action(detail=True, methods=['post'])
    def join(self, request, *args, **kwargs):
        ride = self.get_object()
        serializer_class = self.get_serializer_context()
        serializer = serializer_class(
            ride,
            data={
                'passengers': request.user.pk
            },
            context={'ride': ride, 'circle': self.circle},
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def finish(self, request, *args, **kwargs):
        """llamdo por el porpietario al fionalizar el ride"""
        ride = self.get_object()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(
            ride,
            data={
                'is_active': False,
                'current_time': timezone.now(),
            },
            context=self.get_serializer_context(),
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def rate(self, request, *args, **kwargs):
        """Rate ride."""
        ride = self.get_object()
        serializer_class = self.get_serializer_class()
        context = self.get_serializer_context()
        context['ride'] = ride
        serializer = serializer_class(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        ride = serializer.save()
        data = RideModelSerializer(ride).data
        return Response(data, status=status.HTTP_201_CREATED)
