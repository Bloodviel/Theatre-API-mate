from django.shortcuts import render
from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from theatre.models import (
    Actor,
    Genre,
    TheatreHall
)
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    TheatreHallSerializer
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
