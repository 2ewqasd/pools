from rest_framework import routers
from .views import PoolViewSet
from .views import AnsweredPoolsViewSet

router = routers.DefaultRouter()
router.register(r'pools', PoolViewSet)
router.register(r'answered-pools/(?P<user_id>\d+)',
                AnsweredPoolsViewSet,
                basename="answered-pools")
urlpatterns = router.urls