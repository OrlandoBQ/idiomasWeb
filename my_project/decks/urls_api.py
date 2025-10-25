from rest_framework.routers import DefaultRouter
from .views_api import DeckViewSet, CardViewSet, TagViewSet

router = DefaultRouter()
router.register(r'decks', DeckViewSet, basename='deck')
router.register(r'cards', CardViewSet, basename='card')
router.register(r'tags', TagViewSet, basename='tag')

urlpatterns = router.urls
