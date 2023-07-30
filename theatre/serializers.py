from django.core.exceptions import ValidationError
from rest_framework import serializers

from theatre.models import (
    Actor,
    Genre,
    Ticket,
    TheatreHall,
    Performance,
    Play,
    Reservation
)


class ActorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Actor
        fields = ["id", "first_name", "last_name", "full_name"]


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ["id", "name"]


class TheatreHallSerializer(serializers.ModelSerializer):

    class Meta:
        model = TheatreHall
        fields = ["id", "name", "rows", "seats_in_row", "capacity"]


class PlaySerializer(serializers.ModelSerializer):

    class Meta:
        model = Play
        fields = ["id", "title", "description", "genres", "actors"]


class PlayListSerializer(PlaySerializer):
    genres = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="name"
    )
    actors = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )


class PlayDetailSerializer(PlaySerializer):
    genres = GenreSerializer(many=True, read_only=True)
    actors = ActorSerializer(many=True, read_only=True)

    class Meta:
        model = Play
        fields = ["id", "title", "description", "genres", "actors"]


class GenrePlaysSerializer(PlayListSerializer):

    class Meta:
        model = Play
        fields = ["id", "title"]


class GenreDetailSerializer(GenreSerializer):
    plays = GenrePlaysSerializer(read_only=True, many=True)

    class Meta:
        model = Genre
        fields = ["id", "name", "plays"]


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["performance"].theatre_hall,
            ValidationError
        )
        return data

    class Meta:
        model = Ticket
        fields = ["id", "row", "seat", "performance"]


class TicketSeatSerializer(TicketSerializer):

    class Meta:
        model = Ticket
        fields = ["row", "seat"]


class PerformanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "show_time"]


class PerformanceListSerializer(PerformanceSerializer):
    play = serializers.CharField(
        source="play.title",
        read_only=True
    )
    theatre_hall = serializers.CharField(
        source="theatre_hall.name",
        read_only=True
    )
    theatre_hall_capacity = serializers.IntegerField(
        source="theatre_hall.capacity",
        read_only=True
    )
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Performance
        fields = [
            "id",
            "play",
            "show_time",
            "theatre_hall",
            "theatre_hall_capacity",
            "tickets_available"
        ]


class PerformanceDetailSerializer(PerformanceSerializer):
    play = PlayListSerializer(many=False, read_only=True)
    theatre_hall = TheatreHallSerializer(many=False, read_only=True)
    taken_places = TicketSeatSerializer(many=True, read_only=True, source="tickets")

    class Meta:
        model = Performance
        fields = ["id", "play", "theatre_hall", "taken_places"]


class ReservationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reservation
        fields = ["id", "tickets", "created_at"]
