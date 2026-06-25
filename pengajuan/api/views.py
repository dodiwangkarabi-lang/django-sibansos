from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# model user
from django.contrib.auth.models import User

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from ..models import Pengajuan
from .serializers import (
    PengajuanSerializer, PengajuanCustomSerializer, PengajuanFullSerializer,
    PengajuanBantuanSerializer, VerifikasiPermohonanSerializer, RingkasanSerializer,
    PengajuanRevisiMasyarakatSerializer
)

from rest_framework.parsers import MultiPartParser, FormParser

# services
from pengajuan.services.services import PengajuanService

from django.conf import settings
from django.http import FileResponse, Http404

class PersyaratanBantuanView(APIView):
    def get(self, request):
        file_path = settings.MEDIA_ROOT / "lainnya" / "persyaratan_bantuan.pdf"
        
        if not file_path.exists():
            raise Http404("File tidak ditemukan")
        
        return FileResponse(
            open(file_path, "rb"),
            content_type="application/pdf",
            as_attachment=True,
            filename="persyaratan_bantuan.pdf"
        )
        
        

class PengajuanRevisiMasyarakatView(APIView):
    def post(self, request, pengajuan_id):
        pengajuan = get_object_or_404(Pengajuan, id=pengajuan_id)
        serializer = PengajuanRevisiMasyarakatSerializer(pengajuan, data=request.data)
        if serializer.is_valid():
            serializer.save(pengajuan=pengajuan, status="diproses")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def ringkasan_pengajuan_view(request):
    # user = request.user.masyarakat.pengajuan_set.all()
    # user = User.objects.get(id=3).masyarakat
    # pengajuan = User.objects.get(id=3).masyarakat.pengajuan_set.all()
    pengajuan = request.user.masyarakat.pengajuan_set.all()
    
    # serializer = RingkasanSerializer(user, many=True)
    
    data = {
        "total": pengajuan.count(),
        "disetujui": pengajuan.filter(status__iexact="diterima").count(),
        "ditolak": pengajuan.filter(status__iexact="ditolak").count(),
        "pending": pengajuan.filter(status__iexact="diproses").count(),
        "revisi": pengajuan.filter(status__iexact="revisi").count(),
    }
    # serializer = RingkasanSerializer(data, many=False)
    
    return Response({
        "message": "Ringkasan pengajuan",
        "data": data
    }, status=status.HTTP_200_OK)

class VerifikasiPermohonanView(APIView):
    def post(self, request, pengajuan_id):
        pengajuan = get_object_or_404(Pengajuan, id=pengajuan_id)
        serializer = VerifikasiPermohonanSerializer(pengajuan, data=request.data)
        if serializer.is_valid():
            serializer.save(pengajuan=pengajuan, diverifikasi_oleh=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class DaftarPengajuanView(APIView):
    def get(self, request):
        try:
            masyarakat = request.user.masyarakat
            daftar_pengajuan = (
                Pengajuan.objects
                .filter(masyarakat=masyarakat)
                .select_related("bantuan", "masyarakat")
                .order_by("-tanggal_pengajuan", "-id")
            )
            
            serializer = PengajuanSerializer(daftar_pengajuan, many=True)
        except:
            serializer = PengajuanSerializer([])
            
        payload = {
            "message": "Daftar pengajuan",
            "data": serializer.data
        }
        return Response(payload, status=status.HTTP_200_OK)
    
class DaftarPengajuanMasyarakatView(APIView):
    def get(self, request):
        try:
            masyarakat = request.user.masyarakat
            masyarakat_id = masyarakat.id
            daftar_pengajuan = Pengajuan.objects.filter(masyarakat_id=masyarakat_id)
            daftar_pengajuan = daftar_pengajuan.select_related("bantuan").all()
            serializer = PengajuanCustomSerializer(daftar_pengajuan, many=True)
        except:
            serializer = PengajuanCustomSerializer([])
            
        payload = {
            "message": "Daftar pengajuan per masyarakat",
            "data": serializer.data
        }
        return Response(payload, status=status.HTTP_200_OK)
    

class PengajuanBantuanView(APIView):
    
    parser_classes = (MultiPartParser, FormParser)
    def post(self, request):
        
        if not request.user.is_authenticated:
            return Response({"message": "Anda belum login"}, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = PengajuanBantuanSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(masyarakat=request.user.masyarakat)
            
            payload = {
                "message": "Pengajuan berhasil dikirim",
                "data": serializer.data
            }
            return Response(payload, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PengajuanViewSet(ModelViewSet):
    # queryset = Pengajuan.objects.all() # ini awal
    queryset = Pengajuan.objects.select_related("masyarakat", "bantuan").all()
    serializer_class = PengajuanSerializer
    
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def update(self, request, *args, **kwargs):
        pengajuan = self.get_object()
        
        
        
        serializer = self.get_serializer(pengajuan, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        # logika custom
        pengajuan = serializer.instance
        service = PengajuanService()
        service.verifikasi_pengajuan(pengajuan) # side effect terhadap penerima bantuan
       
        
        return Response({
            "message": "Pengajuan berhasil diupdate",
            "data": serializer.data
        }, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        # print("AUTH HEADER:", request.headers.get("Authorization"))
        # print("USER:", request.user)

        return super().list(request, *args, **kwargs)
    
    
    # def get_queryset(self):
    #     return Pengajuan.objects.filter(id=1)
    
    @action(detail=False, methods=["get"], url_path="riwayat-pengajuan")
    def riwayat_pengajuan(self, request):
        data = self.queryset.filter(masyarakat=request.user.masyarakat)
        serializer = self.get_serializer(data, many=True)
        return Response(serializer.data)
    
    @action(detail=False)
    def full(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    @action(detail=False)
    def masyarakat(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def get_serializer_class(self):
        if self.action == "full":
            return PengajuanFullSerializer
        elif self.action == "masyarakat":
            return PengajuanCustomSerializer
        else:
            return PengajuanSerializer