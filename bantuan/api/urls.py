from rest_framework.routers import DefaultRouter
from .views import (
    BantuanViewSet, KategoriViewSet, PenerimaBantuanView
)
from django.urls import path

router = DefaultRouter()
router.register(r"bantuan", BantuanViewSet)
router.register(r"kategori", KategoriViewSet)

urlpatterns = [
    path("penerima-bantuan/<int:bantuan_id>/", PenerimaBantuanView.as_view(), name="penerima_bantuan_api"),
]

urlpatterns += router.urls