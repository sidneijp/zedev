from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('partners', views.PartnerViewSet)

urlpatterns = router.urls
