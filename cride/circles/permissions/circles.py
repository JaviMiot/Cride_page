


from rest_framework.permissions import BasePermission

from cride.circles.models import Membership

class isCircleAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        """verify user have a membership in the obj

        Args:
            request ([type]): [description]
            view ([type]): [description]
            obj ([type]): [description]
        """
        try:

            Membership.objects.get(
                user=request.user,
                circle=obj,
                is_admin=True,
                is_active=True,
            )
        except Membership.DoesNotExist:
            return False

        return True