

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated

from rest_framework.views import APIView
from rest_framework.response import Response
from accounts.services import registrasi_service
from rest_framework.decorators import api_view, permission_classes

from core.analisis_services import RangkumanData

class RangkumanView(APIView):
    def get(self, request):
        
        data = {
            "message": "berhasil ambil data",
            "data": {
                "total_masyarakat": RangkumanData.total_masyarakat(),
                "total_bantuan": RangkumanData.total_bantuan(),
                "total_penerima_bantuan": RangkumanData.total_penerima_bantuan(),
                
            }
        }
        return Response(data, status=200)

# class MasyarakatViewSet(ModelViewSet):
#     queryset = Masyarakat.objects.all()
#     serializer_class = MasyarakatSerializer
    
#     # authentication_classes = [TokenAuthentication]
#     # permission_classes = [IsAuthenticated]

# class WilayahViewSet(ModelViewSet):
#     queryset = Wilayah.objects.all()
#     serializer_class = WilayahSerializer