from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView
# )

from . import views

urlpatterns = [
    # path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path("login/", views.login_view, name="login"),
]