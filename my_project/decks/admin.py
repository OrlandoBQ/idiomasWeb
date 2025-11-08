from django.contrib import admin
from .models import Deck, Card, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(Deck)
class DeckAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'visibility', 'created_at')
    list_filter = ('visibility',)
    search_fields = ('title', 'description', 'owner__username')
    filter_horizontal = ('tags',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'deck', 'card_type', 'next_review')
    list_filter = ('card_type',)
    search_fields = ('front', 'back')
