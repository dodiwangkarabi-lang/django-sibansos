from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from penyaluran.models import PenerimaBantuan
from .serializers import PenerimaBantuanSerializer

from .services import pdf_report

class PenerimaBantuanViewSet(ModelViewSet):
    queryset = PenerimaBantuan.objects.select_related('masyarakat', 'bantuan')
    serializer_class = PenerimaBantuanSerializer
    
    @action(detail=False, methods=["get"], url_path="pdf")
    def pdf(self, request):
        data = self.get_queryset()
        
        pdf = pdf_report(data)
        
        response = HttpResponse(pdf, content_type="application/pdf")
        response['Content-Disposition'] = 'attachment; filename="laporan.pdf"'
        
        return response
        
        
        
    
# class PenerimaBantuanViewSet(ModelViewSet):
#     queryset = PenerimaBantuan.objects.select_related('masyarakat', 'bantuan')
#     serializer_class = PenerimaBantuanSerializer