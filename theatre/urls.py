from django.urls import path, include
from rest_framework import routers

from theatre.views import (
    ActorViewSet,
    GenreViewSet,
    TicketViewsSet,
    TheatreHallViewSet,
    PerformanceViewSet,
    PlayViewSet,
    ReservationViewSet,
)

router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("theatre_halls", TheatreHallViewSet)
router.register("plays", PlayViewSet)
router.register("performances", PerformanceViewSet)
router.register("tickets", TicketViewsSet)
router.register("reservations", ReservationViewSet)

urlpatterns = [
    path("", include(router.urls))
]
app_name = "theatre"
