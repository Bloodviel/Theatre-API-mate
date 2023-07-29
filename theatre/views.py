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

    @staticmethod
    def _params_in_int(qs):
        return [int(obj_id) for obj_id in qs.split(",")]

    def get_queryset(self):
        queryset = self.queryset
        title = self.request.query_params.get("title")
        genres = self.request.query_params.get("genres")
        actors = self.request.query_params.get("actors")

        if title:
            queryset = queryset.filter(title__icontains=title)

        if genres:
            genres_id = self._params_in_int(genres)
            queryset = queryset.filter(genres__id__in=genres_id)

        if actors:
            actors_id = self._params_in_int(actors)
            queryset = queryset.filter(actors__id__in=actors_id)

        if self.action == "list":
            queryset = queryset.prefetch_related("genres", "actors")

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PlayListSerializer

        if self.action == "retrieve":
            return PlayDetailSerializer

        return PlaySerializer
