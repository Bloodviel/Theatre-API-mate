from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from theatre.models import (
    Actor,
    Genre,
    TheatreHall,
    Play
)
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    TheatreHallSerializer,
    PlaySerializer,
    PlayListSerializer,
    PlayDetailSerializer
)


def index(request):
    return render(request, "theatre/index.html")


class ActorViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer


class GenreViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TheatreHallViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = TheatreHall.objects.all()
    serializer_class = TheatreHallSerializer


class PlayViewSet(
    viewsets.ModelViewSet
):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer

    def get_queryset(self):
        queryset = self.queryset

        if self.action == "list":
            queryset = queryset.prefetch_related("genres", "actors")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailSerializer

        return PlaySerializer
