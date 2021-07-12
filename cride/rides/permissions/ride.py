"""Crea permisos 
    """

from rest_framework.permissions import BasePermission


class IsRideOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.offered_by

class IsNotRideOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return not request.user == obj.offered_by