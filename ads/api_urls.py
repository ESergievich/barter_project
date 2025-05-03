from rest_framework.routers import DefaultRouter

from .api_views import ExchangeProposalViewSet, AdViewSet

router = DefaultRouter()

router.register(r'proposals', ExchangeProposalViewSet, basename='proposal')
urlpatterns = router.urls

router.register(r'ads', AdViewSet, basename='ad')
urlpatterns += router.urls
