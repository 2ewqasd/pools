from rest_framework import routers
from .views import PoolViewSet
from .views import AnsweredPoolsViewSet

router = routers.DefaultRouter()
router.register(r'pools', PoolViewSet, basename="pool")
router.register(r'answered-pools/(?P<user_id>\d+)',
                AnsweredPoolsViewSet,
                basename="answeredpool")
urlpatterns = router.urls
