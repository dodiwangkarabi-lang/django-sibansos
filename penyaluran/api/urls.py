from rest_framework.routers import DefaultRouter
from .views import (
    PenerimaBantuanViewSet
)
from django.urls import path

router = DefaultRouter()
router.register(r"penerima-bantuan", PenerimaBantuanViewSet)

urlpatterns = [
    # path("penerima-bantuan/pdf/", PenerimaBantuanViewSet.as_view({"get": "pdf"}), name="penerima_bantuan_pdf_api"),
]

# urlpatterns = [
#     path("pengajuan-bantuan/", PengajuanBantuanView.as_view(), name="pengajuan_bantuan_api"),
#     path("daftar-pengajuan/", DaftarPengajuanView.as_view(), name="daftar_pengajuan_api"),
#     path("verifikasi-permohonan/<int:pengajuan_id>/", VerifikasiPermohonanView.as_view(), name="verifikasi_pengajuan_api"),
#     path("daftar-pengajuan-masyarakat/", DaftarPengajuanMasyarakatView.as_view(), name="daftar_pengajuan_masyarakat_api"),
# ]

# urlpatterns = router.urls
urlpatterns += router.urls