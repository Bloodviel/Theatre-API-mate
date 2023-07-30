from django.contrib import admin

from theatre.models import (
    Actor,
    Genre,
    Performance,
    Play,
    Ticket,
    TheatreHall,
    Reservation
)


class TicketInLine(admin.TabularInline):
    model = Ticket
    extra = 1


@admin.register(Reservation)
class OrderAdmin(admin.ModelAdmin):
    inlines = (TicketInLine,)


admin.site.register(Actor)
admin.site.register(Genre)
admin.site.register(Performance)
admin.site.register(Play)
admin.site.register(Ticket)
admin.site.register(TheatreHall)
