"""Membership serializers"""

from rest_framework import serializers, status
from cride.circles.models import Membership, Invitation
from cride.users.serializers import UserModelSerializer, profile

from django.utils import timezone


class MembershipModelSerializer(serializers.ModelSerializer):
    """Member model serializer"""
    user = UserModelSerializer(read_only=True)
    invited_by = serializers.StringRelatedField()
    joined_at = serializers.DateTimeField(source='created', read_only=True)

    class Meta:
        model = Membership
        fields = (
            'user',
            'is_admin', 'is_active', 'invited_by',
            'used_invitations', 'remaining_inv',
            'rides_taken', 'rides_offered',
            'joined_at'
        )

        read_only = (
            'user',
            'used_invitations',
            'invited_by',
            'rides_taken', 'rides_offered',
        )


class addMemberSerializer(serializers.Serializer):
    """Agrega un serializer 
    addicion a un nuevo serializer"""

    invitation_code = serializers.CharField(min_length=8)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    def validate_user(self, data):
        """verifica si el usuario no es aun un miembro"""
        circle = self.context['circle']
        user = data

        q = Membership.objects.filter(circle=circle, user=user)
        if q.exists():
            raise serializers.ValidationError('User is already ember of this circle')
        return data

    def validate_invitation_code(self, data):
        """verifica que el codigo existe en el circulo"""
        try:
            invitation = Invitation.objects.get(
                code=data,
                circle=self.context['circle'],
                used=False
            )
        except Invitation.DoesNotExist:
            raise serializers.ValidationError('invalid invitation code')

        self.context['invitation'] = invitation
        return data

    def validate(self, data):
        """veridica capacidad de 
        aceptar un nuevo miembro"""

        circle = self.context['circle']

        if circle.is_limited and circle.members.count() >= circle.members_limit:
            raise serializers.ValidationError('circle has reached its member limit :(')

        return data

    def create(self, data):
        """create new circle member."""
        circle = self.context['circle']
        invitation = self.context['invitation']
        user = data['user']
        now = timezone.now()

        # * crea el miembro
        member = Membership.objects.create(
            user=user,
            profile=user.profiles,
            circle=circle,
            invited_by=invitation.issued_by
        )

        # * actualiza invitatcion
        invitation.used_by = user
        invitation.used = True
        invitation.used_at = now
        invitation.save()

        #* update issuer data
        issuer =  Membership.objects.get(
            user=invitation.issued_by,
            circle=circle,
        )

        issuer.used_invitations += 1
        issuer.remaining_inv -=1
        issuer.save()

        return member