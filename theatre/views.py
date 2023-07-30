from datetime import datetime

from django.db.models import F, Count
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from theatre.models import (
    Actor,
    Genre,
    Ticket,
    TheatreHall,
    Play,
    Performance,
    Reservation,
)
from theatre.permissions import IsAdminOrIsAuthenticatedReadOnly
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


class ActorViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet
):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)


class GenreViewSet(
    viewsets.ModelViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)

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
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)


class PlayViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    GenericViewSet
):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)

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

    @action(
        methods=["POST"],
        detail=True,
        url_path="upload_image"
    )
    def upload_image(self, request, pk=None):
        play = self.get_object()
        serializer = self.get_serializer(play, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="title",
                type=str,
                description="Filter by title (ex. ?title=YourPlay)"
            ),
            OpenApiParameter(
                name="genres",
                type={
                    "type": "list",
                    "items": {"type": "number"}
                },
                description="Filter by genres (ex. ?genres=1,2)"
            ),
            OpenApiParameter(
                name="actors",
                type={
                    "type": "list",
                    "items": {"type": "number"}
                },
                description="Filter by actors (ex. ?actors=1,2)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class PerformanceViewSet(
    viewsets.ModelViewSet
):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)

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

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="play",
                type=int,
                description="Filter by play id (ex. ?play=1)"
            ),
            OpenApiParameter(
                name="date",
                type=OpenApiTypes.DATE,
                description="Filter by date (ex. ?date=2023-07-30)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class TicketViewsSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsAdminOrIsAuthenticatedReadOnly,)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)

        if self.action == "list":
            queryset = queryset.prefetch_related(
                "tickets__performance__theatre_hall",
                "tickets__performance__play"
            )

        return queryset

    def get_serializer_class(self):
        if self.action == "list":
            return ReservationListSerializer

        return ReservationSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
