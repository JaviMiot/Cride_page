"""Permisos para miembros"""

from cride.circles.models.memberships import Membership

from rest_framework.permissions import BasePermission


class IsActiveCircleMember(BasePermission):
    """Permite el acceso solo a los miembros del circulo"""

    def has_permission(self, request, view):
        """Verifica si es activo un miembro del circulo"""
        try:
            Membership.objects.get(
                user=request.user,
                circle=view.circle,
                is_active=True
            )
        except Membership.DoesNotExist:
            return False
        return True


class IsSetMembers(BasePermission):
    "Permite acceso solo ha miembros"

    def has_permission(self, request, view):
        obj = view.get_object()
        return self.has_object_permission(request, view, obj)

    def has_object_permission(self, request, view, obj):
        """Allow access only if member is owned by the requesting user."""
        return request.user == obj.user
