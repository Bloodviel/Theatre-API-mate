from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class TheatreHall(models.Model):
    name = models.CharField(max_length=63)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    class Meta:
        ordering = ["name"]

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=63, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Actor(models.Model):
    first_name = models.CharField(max_length=63)
    last_name = models.CharField(max_length=63)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.first_name + " " + self.last_name


class Play(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default="Beautiful performance")
    genres = models.ManyToManyField(Genre, related_name="plays")
    actors = models.ManyToManyField(Actor, related_name="plays")

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title


class Performance(models.Model):
    play = models.ForeignKey(Play, on_delete=models.CASCADE)
    theatre_hall = models.ForeignKey(TheatreHall, on_delete=models.CASCADE)
    show_time = models.DateTimeField()

    class Meta:
        ordering = ["-show_time"]

    def __str__(self):
        return self.play.title + " " + str(self.show_time)


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return str(self.created_at)


class Ticket(models.Model):
    performance = models.ForeignKey(Performance, on_delete=models.CASCADE)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    row = models.IntegerField()
    seat = models.IntegerField()

    class Meta:
        unique_together = ["performance", "row", "seat"]

    def clean(self):
        for ticket_attr_value, ticket_attr_name, theatre_hall_attr_name in [
            (self.row, "row", "rows"),
            (self.seat, "seat", "seats_in_row")
        ]:
            count_attrs = getattr(
                self.performance.theatre_hall, theatre_hall_attr_name
            )
            if not (1 <= ticket_attr_value <= count_attrs):
                raise ValidationError(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                        f"number must be in available range: "
                        f"(1, {theatre_hall_attr_name}): "
                        f"(1, {count_attrs})"
                    }
                )

    def save(
        self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.full_clean()
        super(Ticket, self).save(
            force_insert, force_update, update_fields
        )

    def __str__(self):
        return (
            f"{str(self.performance)} (row: {self.row}, seat: {self.seat})"
        )
