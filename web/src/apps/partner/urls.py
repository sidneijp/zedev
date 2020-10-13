from . import views, routers

router = routers.DynamicCustomRouter()
router.register('partners', views.PartnerViewSet)
router.add_action(
    'nearest', detail=True, methods=['get'],
    lookup_value=r'(?P<coordinates>-?\d+(.\d+)?,-?\d+(.\d+)?)'
)

urlpatterns = router.urls
