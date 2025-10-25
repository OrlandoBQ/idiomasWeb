from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Deck, Card, Tag
from .serializers import DeckSerializer, CardSerializer, TagSerializer


class DeckViewSet(viewsets.ModelViewSet):
    serializer_class = DeckSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo mostrar las barajas del usuario autenticado
        return Deck.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        user = self.request.user
        visibility = serializer.validated_data.get('visibility', 'private')

        # 🚫 Si es estudiante, no puede crear barajas públicas
        if user.role == 'student' and visibility == 'public':
            raise PermissionDenied("Los estudiantes no pueden publicar barajas públicas.")

        # Asigna el propietario
        serializer.save(owner=user)


class CardViewSet(viewsets.ModelViewSet):
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Solo mostrar tarjetas de las barajas del usuario autenticado
        return Card.objects.filter(deck__owner=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Tag.objects.all()
