from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models import Bantuan, Kategori
from masyarakat.models import Masyarakat
from .serializers import (
    BantuanSerializer, KategoriSerializer, PenerimaBantuanSerializer
)

class BantuanViewSet(ModelViewSet):
    queryset = Bantuan.objects.all()
    serializer_class = BantuanSerializer
    
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    

class KategoriViewSet(ModelViewSet):
    queryset = Kategori.objects.all()
    serializer_class = KategoriSerializer
    
class PenerimaBantuanView(APIView):
    
    def get(self, request, bantuan_id):
        try:
            daftar_penerima = Masyarakat.objects.filter(pengajuan__bantuan_id=bantuan_id).distinct()
            serializer = PenerimaBantuanSerializer(daftar_penerima, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({"message": "Penerima bantuan tidak ditemukan"}, status=status.HTTP_404_NOT_FOUND)
    
    