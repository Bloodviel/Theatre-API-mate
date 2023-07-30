from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from theatre.models import (
    Actor,
    Genre,
    Play,
)
from theatre.serializers import PlayDetailSerializer, PlayListSerializer

PLAY_URL = reverse("theatre-api:play-list")


def detail_url(play_id: int):
    return reverse("theatre-api:play-detail", args=[play_id])


def sample_play(**params):
    defaults = {
        "title": "PlayTest",
        "description": "Simple Play"
    }
    defaults.update(params)

    return Play.objects.create(**defaults)


def sample_genre(**params):
    defaults = {
        "name": "Tragedy",
    }
    defaults.update(params)

    return Genre.objects.create(**defaults)


def sample_actor(**params):
    defaults = {"first_name": "Tom", "last_name": "Timey"}
    defaults.update(params)

    return Actor.objects.create(**defaults)


class UnauthenticatedPlayApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(PLAY_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedPlayApiTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test12345pass"
        )
        self.client.force_authenticate(self.user)

    def test_play_list(self):
        sample_play()
        play_with_actors = sample_play()
        play_with_actors_genres = sample_play()

        genre1 = Genre.objects.create(name="Genre1")
        genre2 = Genre.objects.create(name="Genre2")

        actor1 = Actor.objects.create(first_name="Actor1", last_name="Name1")
        actor2 = Actor.objects.create(first_name="Actor2", last_name="Name2")

        play_with_actors.actors.add(actor1, actor2)
        play_with_actors_genres.actors.add(actor1, actor2)
        play_with_actors_genres.genres.add(genre1, genre2)

        res = self.client.get(PLAY_URL)

        plays = Play.objects.all()
        serializer = PlayListSerializer(plays, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data.get("results"), serializer.data)

    def test_filter_play_by_genres(self):
        play1 = sample_play(title="Play1")
        play2 = sample_play(title="Play2")

        genre1 = sample_genre(name="Genre1")
        genre2 = sample_genre(name="Genre2")

        play1.genres.add(genre1)
        play2.genres.add(genre2)

        play3 = sample_play(title="Play3")

        res = self.client.get(PLAY_URL, {"genres": f"{genre1.id},{genre2.id}"})

        serializer1 = PlayListSerializer(play1)
        serializer2 = PlayListSerializer(play2)
        serializer3 = PlayListSerializer(play3)
        result_data = [dict(i) for i in res.data.get("results")]

        self.assertIn(serializer1.data, result_data)
        self.assertIn(serializer2.data, result_data)
        self.assertNotIn(serializer3.data, result_data)

    def test_retrieve_play(self):
        play = sample_play()
        play.genres.add(sample_genre(name="Genre1"))

        url = detail_url(play.id)
        res = self.client.get(url)

        serializer = PlayDetailSerializer(play)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_play_forbidden(self):
        payload = {
            "title": "Play1",
            "description": "Simple Play"
        }

        res = self.client.post(PLAY_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminApiTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "test1234pass",
            is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_play(self):
        genre1 = sample_genre(name="Genre1")
        genre2 = sample_genre(name="Genre2")

        actor1 = sample_actor(first_name="Actor1", last_name="Test1")
        actor2 = sample_actor(first_name="Actor2", last_name="Test2")

        payload = {
            "title": "Play1",
            "description": "Simple Play",
            "genres": [genre1.id, genre2.id],
            "actors": [actor1.id, actor2.id],
        }

        res = self.client.post(PLAY_URL, payload)
        play = Play.objects.get(id=res.json()["id"])
        genres = play.genres.all()
        actors = play.actors.all()

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(genres.count(), 2)
        self.assertEqual(actors.count(), 2)
        self.assertIn(genre1, genres)
        self.assertIn(genre2, genres)
        self.assertIn(actor1, actors)
        self.assertIn(actor2, actors)

    def test_delete_not_allowed(self):
        play = sample_play()
        url = detail_url(play.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
