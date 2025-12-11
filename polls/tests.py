from datetime import timedelta
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Option, Poll, Vote


class PollsAPITestCase(APITestCase):
    def setUp(self):
        self.poll = Poll.objects.create(
            question="Favorite language?",
            expires_at=timezone.now() + timedelta(days=1),
        )
        self.option_python = Option.objects.create(poll=self.poll, text="Python")
        self.option_js = Option.objects.create(poll=self.poll, text="JavaScript")

    def test_create_poll_with_options(self):
        url = reverse("poll-list")
        payload = {
            "question": "Best framework?",
            "expires_at": (timezone.now() + timedelta(days=2)).isoformat(),
            "options": ["Django", "FastAPI", "Flask"],
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Poll.objects.count(), 2)
        created_poll = Poll.objects.latest("created_at")
        self.assertEqual(created_poll.options.count(), 3)

    def test_vote_once_only(self):
        url = reverse("poll-vote", args=[self.poll.id])
        payload = {"option_id": str(self.option_python.id), "voter_identifier": "user123"}

        first_response = self.client.post(url, payload, format="json")
        self.assertEqual(first_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vote.objects.count(), 1)

        duplicate_response = self.client.post(url, payload, format="json")
        self.assertEqual(duplicate_response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Vote.objects.count(), 1)

    def test_results_accuracy(self):
        Vote.objects.create(poll=self.poll, option=self.option_python, voter_identifier="a")
        Vote.objects.create(poll=self.poll, option=self.option_python, voter_identifier="b")
        Vote.objects.create(poll=self.poll, option=self.option_js, voter_identifier="c")

        url = reverse("poll-results", args=[self.poll.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = {item["option"]: item["votes"] for item in response.data["results"]}
        self.assertEqual(results["Python"], 2)
        self.assertEqual(results["JavaScript"], 1)

