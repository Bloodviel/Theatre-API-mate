from django.urls import path, include
from rest_framework import routers

from theatre.views import (
    index,
    ActorViewSet,
    GenreViewSet,
    TheatreHallViewSet,
    PerformanceViewSet,
    PlayViewSet,
)

router = routers.DefaultRouter()
router.register("actors", ActorViewSet)
router.register("genres", GenreViewSet)
router.register("theatre_halls", TheatreHallViewSet)
router.register("plays", PlayViewSet)
router.register("performances", PerformanceViewSet)

urlpatterns = [
    path("", index, name="index"),
    path("theatre/", include(router.urls))
]
app_name = "theatre"
