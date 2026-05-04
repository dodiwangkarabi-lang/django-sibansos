from rest_framework import serializers
from ..models import Pengajuan

from bantuan.api.serializers import BantuanSerializer
from masyarakat.api.serializers import MasyarakatSerializer
from masyarakat.models import Masyarakat
from bantuan.models import Bantuan

class VerifikasiPermohonanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengajuan
        fields = ["status", "catatan"]
        
class PengajuanRevisiMasyarakatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengajuan
        fields = ["status", "file_pengajuan"]

class PengajuanBantuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengajuan
        fields = ["bantuan", "file_pengajuan", "catatan"]   
        
class PengajuanSerializer(serializers.ModelSerializer):
    bantuan = BantuanSerializer(read_only=True)
    masyarakat = MasyarakatSerializer(read_only=True)
    
    bantuan_id = serializers.PrimaryKeyRelatedField(
        queryset=Bantuan.objects.all(),
        source='bantuan',
        write_only=True
    )
    masyarakat_id = serializers.PrimaryKeyRelatedField(
        queryset=Masyarakat.objects.all(),
        source='masyarakat',
        write_only=True
    )
    
    class Meta:
        model = Pengajuan
        fields = '__all__'
        
class PengajuanFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengajuan
        fields = '__all__'
        
class PengajuanCustomSerializer(serializers.ModelSerializer):
    bantuan = BantuanSerializer(read_only=True)
    masyarakat = MasyarakatSerializer(read_only=True)
    
    class Meta:
        model = Pengajuan
        fields = ['id', 'status', 'catatan', 'bantuan', 'file_pengajuan', 'tanggal_pengajuan', 'tanggal_diperbarui']

class RingkasanSerializer(serializers.Serializer):
    total = serializers.IntegerField()
    diproses = serializers.IntegerField()
    diterima = serializers.IntegerField()
    ditolak = serializers.IntegerField()
