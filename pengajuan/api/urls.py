from rest_framework.routers import DefaultRouter
from .views import (
    PengajuanViewSet, PengajuanBantuanView, DaftarPengajuanView,
    VerifikasiPermohonanView, DaftarPengajuanMasyarakatView,
    ringkasan_pengajuan_view, PengajuanRevisiMasyarakatView
)
from django.urls import path

router = DefaultRouter()
router.register(r"pengajuan", PengajuanViewSet)

urlpatterns = [
    path("pengajuan-bantuan/", PengajuanBantuanView.as_view(), name="pengajuan_bantuan_api"),
    path("daftar-pengajuan/", DaftarPengajuanView.as_view(), name="daftar_pengajuan_api"),
    path("verifikasi-permohonan/<int:pengajuan_id>/", VerifikasiPermohonanView.as_view(), name="verifikasi_pengajuan_api"),
    path("daftar-pengajuan-masyarakat/", DaftarPengajuanMasyarakatView.as_view(), name="daftar_pengajuan_masyarakat_api"),
    path("ringkasan-pengajuan/", ringkasan_pengajuan_view, name="ringkasan_pengajuan_api"),
    path("pengajuan-revisi-masyarakat/<int:pengajuan_id>/", PengajuanRevisiMasyarakatView.as_view(), name="pengajuan_revisi_masyarakat_api"),
]

urlpatterns += router.urls