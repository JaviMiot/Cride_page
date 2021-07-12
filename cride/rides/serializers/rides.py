from cride.circles.permissions import memberships
from cride.rides import serializers


from rest_framework import serializers
from cride.rides.models import Ride

from datetime import timedelta
from django.utils import timezone

from cride.circles.models import Membership
from cride.users.serializers import UserModelSerializer
from cride.users.models import Users


class CreateRidesSerializer(serializers.ModelSerializer):
    offered_by = serializers.HiddenField(default=serializers.CurrentUserDefault())
    available_seats = serializers.IntegerField(min_value=1, max_value=15)

    class Meta:
        """meta class"""
        model = Ride
        exclude = ['passengers', 'rating', 'is_active', 'offered_in']

    def validate_departure_date(self, data):
        """verifica si no se paso un viaje"""
        min_date = timezone.now() + timedelta(minutes=20)

        if data < min_date:
            raise serializers.ValidationError('Departure time must be alt least pass the mexr 30 minustes windows')

        return data

    def validate(self, data):
        """ verifica quie sea miembro y el mismo que hizo el request"""

        if self.context['request'].user != data['offered_by']:
            raise serializers.ValidationError('rides offered on behalf of others are not allowed')

        user = data['offered_by']
        circle = self.context['circle']

        try:
            membership = Membership.objects.get(
                user=user,
                circle=circle,
                is_active=True)
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is not an active member of the circle.')

        if data['arrival_date'] <= data['departure_date']:
            raise serializers.ValidationError('Departure date must happen after arrival date.')

        self.context['membership'] = membership
        return data

    def create(self, data):
        circle = self.context['circle']
        ride = Ride.objects.create(**data, offered_in=circle)

        circle.rides_offered += 1
        circle.save()

        membership = self.context['membership']
        membership.rides_offered += 1
        membership.save()

        profile = data['offered_by'].profiles
        profile.rides_offered += 1
        profile.save()

        return ride


class RideModelSerializer(serializers.ModelSerializer):
    """Ride model serializer."""
    offered_by = UserModelSerializer(read_only=True)
    offered_in = serializers.StringRelatedField()

    passengers = UserModelSerializer(read_only=True, many=True)

    class Meta:
        model = Ride
        fields = '__all__'
        read_only_fields = (
            'offered_by',
            'offered_in',
            'rating'
        )

    def update(self, instance, data):
        """permite actualizar antes del dia de salida"""
        now = timezone.now()
        if instance.departure_date <= now:
            raise serializers.ValidationError('ongoing rides cannot be modified')
        return super(RideModelSerializer, self).update(instance, data)


class JoinRideSerializer(serializers.ModelSerializer):
    """Join ride serializer"""
    passengers = serializers.IntegerField()

    class Meta:
        model = Ride
        fields = ('passengers',)

    def validate_passengers(self, data):
        """verifica si es parte dle circulo"""
        try:
            user = Users.objects.get(pk=data)
        except Users.DoesNotExist:
            raise serializers.ValidationError('Invalid passengere.')

        circle = self.context['circle']
        try:
            membership = Membership.objects.get(
                user=user,
                circle=circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            raise serializers.ValidationError('User is no an activbe member of the circle')
        
        if not Membership.objects.filter(user=user, circle=circle, is_active=True).exists():
            raise serializers.ValidationError('user is not an activa member of the circle')

        self.context['user'] = user
        self.context['member'] = membership
        return data

    def validate(self, data):
        """verifica si el ride permite nuevos pasajheros"""
        offset = timezone.now() + timedelta(minutes=10)
        ride = self.context['ride']
        if ride.departure_date <= offset:
            raise serializers.ValidationError("you can't join this ride now")

        if ride.available_seats < 1:
            raise serializers.ValidationError('Ride is already full!')

        if Ride.objects.filter(passengers__pk=data['passengers']):
            raise serializers.ValidationError('Passengers is already in this trip')

        return data

    def update(self, instance, data):
        """agrega un pasajero al ride y actualiza estado"""
        ride = self.context['ride']
        circle = self.context['circle']
        user = self.context['user']

        ride.passengers.add(user)

        # * profile
        profile = user.profiles
        profile.rides_taken += 1
        profile.save()

        # * memberships

        member = self.context['member']
        member.rides_taken += 1
        member.save()

        # * circles
        circle = self.context['circle']
        circle.rides_taken += 1
        circle.save()

        #* actualiza asientos
        ride.passengers.add(user)
        ride.availiable_seats -= 1
        ride.save()

        return ride

class EndRideSerializer(serializers.ModelSerializer):
    """emd ride serializer"""
    current_time = serializers.DateTimeField()

    class Meta:
        model =Ride
        fields = ('is_active','current_time')

    def validate_current_time(self,data):
        """verify ride have indeed started"""
        ride = self.context['view'].get_object()
        if data <= ride.departure_date:
            raise serializers.ValidationError('Ride has not startet yet')

    