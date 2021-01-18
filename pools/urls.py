from rest_framework import routers
from .views import PoolViewSet

router = routers.DefaultRouter()
router.register(r'pools', PoolViewSet)
urlpatterns = router.urls