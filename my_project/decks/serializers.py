from rest_framework import serializers
from .models import Deck, Card, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = [
            'id', 'deck', 'card_type', 'front', 'back',
            'ease_factor', 'interval', 'next_review',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['ease_factor', 'interval', 'next_review', 'created_at', 'updated_at']


class DeckSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)
    cards_count = serializers.IntegerField(source='cards.count', read_only=True)

    class Meta:
        model = Deck
        fields = [
            'id', 'owner', 'title', 'description', 'visibility',
            'tags', 'cards_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'created_at', 'updated_at']
