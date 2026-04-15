from rest_framework.routers import DefaultRouter
from .views import MasyarakatViewSet, WilayahViewSet

router = DefaultRouter()
router.register(r'masyarakat', MasyarakatViewSet)
router.register(r'wilayah', WilayahViewSet)
urlpatterns = router.urls
