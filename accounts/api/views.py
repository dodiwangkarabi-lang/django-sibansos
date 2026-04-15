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