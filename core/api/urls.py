from django.urls import path
from .views import RangkumanView

urlpatterns = [
    path("rangkuman/", RangkumanView.as_view(), name="rangkuman"),
]
