from rest_framework import serializers
from ..models import Masyarakat, Wilayah

class MasyarakatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Masyarakat
        fields = '__all__'
        
class WilayahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wilayah
        fields = '__all__'