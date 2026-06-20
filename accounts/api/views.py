from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.services import registrasi_service
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .serializers import (
    ProfileSerializer, UserSerializer, MasyarakatSerializer, UserApiSerializer,
    ChangePasswordSerializer
)
from django.contrib.auth.models import User

from masyarakat.models import Masyarakat, Wilayah

from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView

# serializer
from .serializers import CustomTokenObtainPairSerializer, CustomUserSerializer, LupaPasswordSerialzer

# usecase
from accounts.usecases.auth import Auth

class DetailAkunBelumAktifView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, user_id=None):
        user = User.objects.select_related("masyarakat").get(id=user_id)
        serializers = CustomUserSerializer(user, context={"request": request})
        
        return Response({
            "data": serializers.data,
            "success": True,
            "message": "Detail akun belum aktif"
        })

class DaftarAkunBelumAktifView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user = User.objects.select_related("masyarakat").filter(is_active=False).all()
        serializers = CustomUserSerializer(user, many=True, context={"request": request})
        
        return Response({
            "data": serializers.data,
            "success": True,
            "message": "Daftar akun belum aktif"
        })
        

class LupaSandiView(APIView):
    def get(self, request):
        pass
    
    def post(self, request):
        # print("post lupa sandi")
        mydata = ""
        data = request.data
        serializer = LupaPasswordSerialzer(data=data)
        is_valid = serializer.is_valid()
        if is_valid:
            data = serializer.validated_data
            email = data.get("email")
            user = User.objects.filter(email=email).first()
            uc = Auth()
            uc.lupa_password(user)
            return Response({
                "message": "reset password berhasil dikirim",
                "data": mydata,
                "success": True
            }, status=200)
            
        else:
            is_succes = False
            mydata = serializer.errors
            
            return Response({
                "message": "reset password gagal dikirim",
                "data": mydata,
                "success": False
            }, status=400)
            

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def profile(request):
    user = request.user
    
    # masyarakat = user.masyarakat
    masyarakat = getattr(user, "masyarakat", None)
    
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "groups": [group.name for group in user.groups.all()],
        "masyarakat": ProfileSerializer(masyarakat).data if masyarakat else None
    })
    
class GantiSandiView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            data = serializer.validated_data.copy()
            data["password"] = data["new_password1"]
            auth_uc = Auth()
            auth_uc.ganti_password(request.user, data["password"])
            
            # serializer.save()
            return Response({"message": "Password berhasil diganti"}, status=200)
        return Response(serializer.errors, status=400)
    
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class UserViewSet(ModelViewSet):
    queryset = User.objects.prefetch_related('groups').select_related('masyarakat')
    serializer_class = UserApiSerializer

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # profile = request.user.masyarakat # instance Masyarakt (one)
        try:
            profile = Masyarakat.objects.select_related("user").get(user=request.user)
        except Masyarakat.DoesNotExist:
            return Response({
                "detail": "Profil tidak ditemukan"
            }, status=404)
        
        data = ProfileSerializer(profile).data
        return Response({"data": data, "message": "Profil berhasil didapatkan"}, status=200)
    
    def put(self, request):
        try:
            profile = Masyarakat.objects.select_related("user").get(user=request.user)
        except Masyarakat.DoesNotExist:
            return Response({
                "detail": "Profil tidak ditemukan"
            }, status=404)
        
        serializer = ProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"data": serializer.data, "message": "Profil berhasil diupdate"}, status=200)
        else:
            return Response({"errors": serializer.errors, "message": "Profil gagal diupdate"}, status=400)
        

class DeleteAkunView(APIView):
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, user_id):
        user = User.objects.get(id=user_id)
        
        uc = Auth()
        user = uc.hapus_akun(user)
        if user:
            return Response({
                "message": "Akun berhasil dihapus",
                "data": None,
                "success": True
            }, status=200)
        else:
            return Response({
                "message": "Akun gagal dihapus",
                "success": False,
                "data": None
            }, status=400)

class AktivasiAkunView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # is_active = request.data.get("is_active")
        user_id = request.data.get("user_id")
        user = User.objects.get(id=user_id)
        
        # print(user.is_active)
        
        uc = Auth()
        user = uc.aktifkan_akun(user)
        if user:
            return Response({
                "message": "Akun berhasil diaktifkan",
                "data": None,
                "success": True
            }, status=200)
        else:
            return Response({
                "message": "Akun gagal diaktifkan",
                "success": False,
                "data": None
            }, status=400)
        
class RegistrasiAkunView(APIView):
    def post(self, request):
        form_data = request.data
        
        user_serializer = UserSerializer(data=form_data)
        masyarakat_serializer = MasyarakatSerializer(data=form_data)
        
        user_valid = user_serializer.is_valid()
        masyarakat_valid = masyarakat_serializer.is_valid()

        if user_valid and masyarakat_valid:
            data = {**user_serializer.validated_data, **masyarakat_serializer.validated_data}
            uc = Auth()
            user, masyarakat = uc.registrasi_akun(data)
            
            data = {
                "message": "Registrasi berhasil",
                "data": {
                    "user": user_serializer.data,
                    "masyarakat": masyarakat_serializer.data
                },
                "success": True
            }
            # print("berhasil")
        else:
            data = {
                "errors": {
                    "user": user_serializer.errors,
                    "masyarakat": masyarakat_serializer.errors
                },
                "success": False,
                "message": "Registrasi gagal"
            }
            # print("gagal")
        return Response(data, status=201)

class RegistrasiView(APIView):
    def post(self, request):
        # data dari user
        user_serializer = UserSerializer(data=request.data)
        masyarakat_serializer = MasyarakatSerializer(data=request.data)
        
        user_valid = user_serializer.is_valid()
        masyarakat_valid = masyarakat_serializer.is_valid()
        
        if user_valid and masyarakat_valid:
            payload = {
                "username": user_serializer.validated_data["username"],
                "password": user_serializer.validated_data["password"],
                "nik": masyarakat_serializer.validated_data["nik"],
                "nama": masyarakat_serializer.validated_data["nama"],
            }
            user = registrasi_service(payload)
            
            data = {
                "message": "Registrasi berhasil",
                "data": {
                    "user": user_serializer.data,
                    "masyarakat": masyarakat_serializer.data
                }
            }
            return Response(data, status=201)
      
        else:
            data = {
                "message": "Registrasi gagal",
                "errors": {
                    "user": user_serializer.errors,
                    "masyarakat": masyarakat_serializer.errors
                }
            }
            return Response(data, status=400)
        
class ChangePasswordView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        
        serializer = ChangePasswordSerializer(data=request.data, context={"request": request})
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data["new_password1"])
            user.save()
            return Response({"message": "Password berhasil diubah"}, status=200)
        else:
            return Response({"errors": serializer.errors}, status=400)