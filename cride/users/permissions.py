""""Se crea los permisos de usuario"""

from rest_framework.permissions import BasePermission


class IsAccountOwner(BasePermission):

    def has_object_permission(self,request,view,obj):
        """chequea obj y usuario son los mismos"""

        return request.user == obj