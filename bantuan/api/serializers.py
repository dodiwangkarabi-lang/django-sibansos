from rest_framework import serializers
from bantuan.models import Bantuan, Kategori
from masyarakat.models import Masyarakat

class BantuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bantuan
        fields = "__all__" 
        
class KategoriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategori
        fields = "__all__"
        
class PenerimaBantuanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Masyarakat
        fields = "__all__"