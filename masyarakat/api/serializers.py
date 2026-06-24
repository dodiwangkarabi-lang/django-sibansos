from rest_framework import serializers
from ..models import Masyarakat, Wilayah
from accounts.api.serializers import UserProfileSerializer

class MasyarakatSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    email = serializers.EmailField(write_only=True, required=False)
    
    class Meta:
        model = Masyarakat
        fields = '__all__'
        
    def update(self, instance, validated_data):
        email = validated_data.pop("email", None)

        # update model masyarakat
        instance = super().update(instance, validated_data)

        # update email user jika dikirim
        if email:
            instance.user.email = email
            instance.user.save(update_fields=["email"])

        return instance
        
class WilayahSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wilayah
        fields = '__all__'