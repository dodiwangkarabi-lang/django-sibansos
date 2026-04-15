from masyarakat.api.serializers import MasyarakatSerializer
from bantuan.api.serializers import BantuanSerializer
from penyaluran.models import PenerimaBantuan
from masyarakat.models import Masyarakat
from bantuan.models import Bantuan

from rest_framework import serializers

class PenerimaBantuanSerializer(serializers.ModelSerializer):
    masyarakat = MasyarakatSerializer(read_only=True)
    bantuan = BantuanSerializer(read_only=True)
    
    masyarakat_id = serializers.PrimaryKeyRelatedField(
        queryset=Masyarakat.objects.all(),
        source='masyarakat',
        write_only=True
    )
    
    bantuan_id = serializers.PrimaryKeyRelatedField(
        queryset=Bantuan.objects.all(),
        source='bantuan',
        write_only=True
    )
    
    class Meta:
        model = PenerimaBantuan
        fields = "__all__"