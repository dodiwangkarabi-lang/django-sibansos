from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from penyaluran.models import PenerimaBantuan
from .serializers import PenerimaBantuanSerializer

class PenerimaBantuanViewSet(ModelViewSet):
    queryset = PenerimaBantuan.objects.select_related('masyarakat', 'bantuan')
    serializer_class = PenerimaBantuanSerializer