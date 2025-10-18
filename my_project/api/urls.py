from django.urls import path, include
from users import urls_api as user_urls
from decks import urls_api as deck_urls

urlpatterns = [
    path('users/', include(user_urls)),
    path('', include(deck_urls)),
]
