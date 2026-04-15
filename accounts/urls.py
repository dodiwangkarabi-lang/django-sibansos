from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('login')), name='logout'),
    path("login/", views.login_view, name="login"),
]