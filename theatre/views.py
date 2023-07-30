from datetime import datetime

from django.db.models import F, Count
from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from theatre.models import (
    Actor,
    Genre,
    Ticket,
    TheatreHall,
    Play,
    Performance,
    Reservation,
)
from theatre.serializers import (
    ActorSerializer,
    GenreSerializer,
    GenreDetailSerializer,
    TicketSerializer,
    TheatreHallSerializer,
    PerformanceSerializer,
    PerformanceListSerializer,
    PerformanceDetailSerializer,
    PlaySerializer,
    PlayListSerializer,
    PlayDetailSerializer,
    ReservationSerializer,
    ReservationListSerializer,
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
    viewsets.ModelViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_serializer_class(self):
        if self.action == "retrieve":
            return GenreDetailSerializer

        return GenreSerializer


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


class PerformanceViewSet(
    viewsets.ModelViewSet
):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

    def get_queryset(self):
        queryset = self.queryset

        play = self.request.query_params.get("play")
        date = self.request.query_params.get("date")

        if play:
            queryset = queryset.filter(play__id=play)

        if date:
            date = datetime.strptime(date, "%Y-%m-%d").date()
            queryset = queryset.filter(show_time__date=date)

        if self.action == "list":
            queryset = (
                Performance.objects.select_related("play", "theatre_hall")
                .annotate(
                    tickets_available=F("theatre_hall__rows")
                    * F("theatre_hall__seats_in_row")
                    - Count("tickets")

                )
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return PerformanceListSerializer

        if self.action == "retrieve":
            return PerformanceDetailSerializer

        return PerformanceSerializer


class TicketViewsSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
