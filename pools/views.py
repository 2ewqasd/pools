from rest_framework import viewsets

from .models import Pool
from .serializers import PoolSerializer
from .serializers import PoolExtendentSerializer


class PoolViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A simple ViewSet for viewing pools.
    """
    queryset = Pool.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return PoolSerializer
        return PoolExtendentSerializer