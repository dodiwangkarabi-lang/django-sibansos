from rest_framework import serializers
from masyarakat.models import Masyarakat, Wilayah
from django.contrib.auth.models import User, Group
from django.db import transaction


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password_confirm"]

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        password_confirm = data.get("password_confirm")

        print("password dan password confirm")
        print(password, password_confirm)

        if password != password_confirm:
            raise serializers.ValidationError("Password tidak sama")

        return data


class MasyarakatSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)

    class Meta:
        model = Masyarakat
        fields = ["nik", "nama"]

    def validate(self, data):
        nik = data.get("nik")
        nama = data.get("nama")

        # validasi nik
        if nik and len(nik) != 16:
            raise serializers.ValidationError("NIK harus 16 digit")

        # validasi nama
        if nama and nama.lower() == "admin":
            raise serializers.ValidationError("Nama tidak boleh admin")

        return data


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = "__all__"


class UserApiSerializer(serializers.ModelSerializer):
    # groups = serializers.StringRelatedField(read_only=True, many=True)
    masyarakat = MasyarakatSerializer(read_only=True)
    groups = serializers.SlugRelatedField(many=True, read_only=True, slug_field="name")

    class Meta:
        model = User
        fields = ["id", "username", "email", "groups", "masyarakat"]


class ProfileSerializer(serializers.ModelSerializer):
    # user = UserApiSerializer(read_only=True)
    username = serializers.CharField(
        source="user.username",
        required=False,
        allow_null=True,
        allow_blank=True
    )

    class Meta:
        model = Masyarakat
        fields = [
            "id",
            "nik",
            "nama",
            # "user",
            "no_kk",
            "jenis_kelamin",
            "tempat_lahir",
            "tanggal_lahir",
            "alamat",
            "rt",
            "rw",
            "desa",
            "kecamatan",
            "kabupaten",
            "provinsi",
            "no_hp",
            "wilayah",
            "created_at",
            "updated_at",
            "username"
        ]
        
    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})

        # update profile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # update username
        user = instance.user
        if 'username' in user_data:
            user.username = user_data['username']
            user.save()

        return instance
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password1 = serializers.CharField(required=True)
    new_password2 = serializers.CharField(required=True)
    
    def validate(self, data):
        user = self.context['request'].user

        # cek password lama
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError({
                "old_password": "Password lama salah"
            })

        # cek password baru sama
        if data['new_password1'] != data['new_password2']:
            raise serializers.ValidationError({
                "new_password2": "Password baru tidak sama"
            })

        return data
