from rest_framework.routers import DefaultRouter
from .views import (
    RegistrasiView, ProfileView, UserViewSet, profile, ChangePasswordView
)

from . import views

from django.urls import path

router = DefaultRouter()
router.register(r"user", UserViewSet)

urlpatterns = [
    path('detail-akun-belum-aktif/<int:user_id>/', views.DetailAkunBelumAktifView.as_view(), name='detail_akun_belum_aktif'),
    path('daftar-akun-belum-aktif/', views.DaftarAkunBelumAktifView.as_view(), name='daftar_akun_belum_aktif'),
    path('lupa-sandi/', views.LupaSandiView.as_view(), name='lupa_sandi'),
    path('ganti-sandi/', views.GantiSandiView.as_view(), name='ganti_sandi'),
    path('registrasi-akun/', views.RegistrasiAkunView.as_view(), name='registrasi_akun'),
    path('delete-akun/<int:user_id>/', views.DeleteAkunView.as_view(), name='delete_akun'),
    path('aktivasi-akun/', views.AktivasiAkunView.as_view(), name='aktivasi_akun'),
    path('registrasi/', RegistrasiView.as_view(), name='registrasi'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('me/', profile, name='me'),
]

urlpatterns += router.urls
