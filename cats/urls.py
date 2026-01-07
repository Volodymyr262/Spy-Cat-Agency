"""
URL configuration for cats app.
"""

from rest_framework.routers import DefaultRouter

from cats.views import SpyCatViewSet

router = DefaultRouter()
router.register(r"", SpyCatViewSet, basename="spycat")

urlpatterns = router.urls
