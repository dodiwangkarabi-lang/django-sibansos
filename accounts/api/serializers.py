from rest_framework import serializers
from masyarakat.models import Masyarakat, Wilayah
from django.contrib.auth.models import User, Group
from django.db import transaction

from django.contrib.auth import authenticate

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from rest_framework import serializers

class LupaPasswordSerialzer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class ResetPasswordSerializer(serializers.Serializer):
    password1 = serializers.CharField(
        write_only=True,
        min_length=8
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=8
    )

    def validate(self, data):
        if data["password1"] != data["password2"]:
            raise serializers.ValidationError(
                "Password dan konfirmasi password tidak sama."
            )
        return data

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    
    def validate(self, attrs):
        # authenticate user (pakai bawaan SimpleJWT)
        # self.user = self.authenticate(attrs)
        user = authenticate(
            username = attrs.get("username"),
            password = attrs.get("password"),
        )

        if not user:
            raise serializers.ValidationError({
                "detail": "Username atau password salah, atau akun Anda belum aktif. Silakan hubungi admin."
            })

        # if not user.is_active:
        #     raise serializers.ValidationError({
        #         "detail": "Akun Anda belum aktif. Silakan hubungi admin."
        #     })

        # pakai cara resmi SimpleJWT
        refresh = self.get_token(user)

        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "email": user.email
        }

        return data


class UserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "password_confirm", "email"]

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
        fields = ["nik", "nama", "no_hp", "foto_ktp"]

    def validate(self, data):
        nik = data.get("nik")
        nama = data.get("nama")
        no_hp = data.get("no_hp")
        foto_ktp = data.get("foto_ktp")
        
        # validasi foto ktp
        if foto_ktp and len(foto_ktp) > 3000000:
            raise serializers.ValidationError("Foto KTP tidak boleh lebih dari 3 MB")
        
        # validasi no hp
        if no_hp and len(no_hp) != 12:
            raise serializers.ValidationError("No HP harus 12 digit")

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
        """
        

        Args:
            data (_type_): _description_

        Raises:
            serializers.ValidationError: _description_
            serializers.ValidationError: _description_

        Returns:
            _type_: _description_
            
        Example:
            serializer = ChangePasswordSerializer(data=request.data, context={"request": request})

        """
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


        
class CustomMasyarakatSerializer(serializers.ModelSerializer):
    foto_ktp = serializers.SerializerMethodField()
    
    class Meta:
        model = Masyarakat
        fields = '__all__'
        
    def get_foto_ktp(self, obj):
        request = self.context.get("request")
        
        if obj.foto_ktp:
            return request.build_absolute_uri(obj.foto_ktp.url)
        
        return None
        
class CustomUserSerializer(serializers.ModelSerializer):
    masyarakat = CustomMasyarakatSerializer(read_only=True)
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'masyarakat']


class MasyarkatSerializerFull(serializers.ModelSerializer):
    user = CustomUserSerializer(read_only=True)
    
    class Meta:
        model = Masyarakat
        fields = '__all__'