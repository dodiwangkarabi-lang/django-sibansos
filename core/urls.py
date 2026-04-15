from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView

from . import views

urlpatterns = [
    path("dashboard_masyarakat/", views.dashboard_masyarakat, name="dashboard_masyarakat"),
    path("dashboard_admin/", views.dashboard_admin, name="dashboard_admin"),
    path("pengajuan_detail/<int:pengajuan_id>/", views.pengajuan_detail_view, name="pengajuan_detail"),
    path("api-core/", include("core.api.urls")),
    path('', views.index, name='index'),
]