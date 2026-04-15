from rest_framework.viewsets import ModelViewSet
from .serializers import MasyarakatSerializer, WilayahSerializer
from ..models import Masyarakat, Wilayah

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class MasyarakatViewSet(ModelViewSet):
    queryset = Masyarakat.objects.all()
    serializer_class = MasyarakatSerializer
    
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

class WilayahViewSet(ModelViewSet):
    queryset = Wilayah.objects.all()
    serializer_class = WilayahSerializer