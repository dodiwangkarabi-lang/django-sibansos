from rest_framework.routers import DefaultRouter
from .views import (
    RegistrasiView, ProfileView, UserViewSet, profile, ChangePasswordView
)

from django.urls import path

router = DefaultRouter()
router.register(r"user", UserViewSet)

urlpatterns = [
    path('registrasi/', RegistrasiView.as_view(), name='registrasi'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('me/', profile, name='me'),
]

urlpatterns += router.urls
