
#* Circles views 

#* django rest 
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from cride.circles.models import Circle

from cride.circles.serializers import CircleModelSerializer

from cride.circles.models import Membership
class CirclesViewSet(viewsets.ModelViewSet):
    """circle view set

    Args:
        viewsets ([type]): [description]
    """

    queryset = Circle.objects.all()
    serializer_class = CircleModelSerializer
    #* Para ver si esta con token el usuario
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """rtestick publict only"""

        queryset = Circle.objects.all()

        if self.action == 'list':
            return queryset.filter(is_public=True)

        return queryset

    def perform_create(self,serializer):
        """Assign circle admin

        Args:
            serializer ([type]): [description]
        """

        circle =  serializer.save()
        user = self.request.user
        profile = user.profiles
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_inv=10
        )
