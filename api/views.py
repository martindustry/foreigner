from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)

from api.models import Box, Card, Deck
from api.permissions import IsBoxAuthor, IsCardAuthor, IsDeckAuthor
from api.serializers import (
    BoxSerializer,
    CardDetailSerializer,
    CardListSerializer,
    DeckSerializer,
)


class DeckListView(ListCreateAPIView):
    serializer_class = DeckSerializer

    def get_queryset(self):
        return Deck.objects.filter(author=self.request.user)


class DeckDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Deck.objects.all()
    serializer_class = DeckSerializer
    permission_classes = [IsDeckAuthor]


class BoxListView(ListAPIView):
    serializer_class = BoxSerializer

    def get_queryset(self):
        queryset = Box.objects.filter(deck__author=self.request.user)
        deck_id = self.request.query_params.get("deck")
        if deck_id is not None:
            queryset = queryset.filter(deck__id=deck_id)
        return queryset


class BoxDetailView(RetrieveAPIView):
    serializer_class = BoxSerializer
    permission_classes = [IsBoxAuthor]
    queryset = Box.objects.all()


class CardListView(ListCreateAPIView):
    serializer_class = CardListSerializer

    def get_queryset(self):
        queryset = Card.objects.filter(deck__author=self.request.user)
        deck_id = self.request.query_params.get("deck")
        box_id = self.request.query_params.get("box")
        if deck_id is not None:
            queryset = queryset.filter(deck__id=deck_id)
        if box_id is not None:
            queryset = queryset.filter(box__id=box_id)
        return queryset


class CardDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Card.objects.all()
    serializer_class = CardDetailSerializer
    permission_classes = [IsCardAuthor]
