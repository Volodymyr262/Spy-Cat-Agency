"""
URL configuration for cats app.
"""

from rest_framework.routers import DefaultRouter

from cats.views import MissionViewSet, SpyCatViewSet, TargetViewSet

router = DefaultRouter()
router.register(r"cats", SpyCatViewSet, basename="spycat")
router.register(r"missions", MissionViewSet, basename="mission")
router.register(r"targets", TargetViewSet, basename="target")
urlpatterns = router.urls
