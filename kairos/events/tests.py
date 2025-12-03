from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from events.models import Event
from datetime import datetime


class CreateEventTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="m", password="1234")
        self.client.login(username="m", password="1234")

    def test_create_event(self):
        """POST /events/create/ should create an event and redirect to slug-based URL"""

        url = reverse("events:create")

        data = {
            "event_id": "my-test-event",
            "title": "My Event",
            "description": "Some description",
            "start_time": "2025-01-12T18:30",
            "end_time": "2025-01-12T20:00",
        }

        response = self.client.post(url, data)

        # Should redirect to /events/<slug>/
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/events/my-test-event/")

        # Validate database record
        event = Event.objects.get(event_id="my-test-event")
        self.assertEqual(event.title, "My Event")
        self.assertEqual(event.body, "Some description")
        self.assertEqual(event.start_date.isoformat(), "2025-01-12")
        self.assertEqual(event.start_time.isoformat(), "18:30:00")
        self.assertEqual(event.end_time.isoformat(), "20:00:00")

    def test_events_list(self):
        test_user = User.objects.create_user(username='event_tester1', password='pass12345')

        Event.objects.create(
            title="Test A",
            body="desc",
            event_id="a",
            creator=test_user,
            start_date=datetime(2025, 1, 1).date(),
            start_time=datetime(2025, 1, 1, 10),
            end_date=datetime(2025, 1, 1).date(),
            end_time=datetime(2025, 1, 1, 11),
        )

        response = self.client.get(reverse("events:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test A")

    def test_event_search_filter(self):
        test_user = User.objects.create_user(username='event_tester2', password='pass12345')

        Event.objects.create(
            title="Soccer Night",
            body="fun",
            event_id="soccer",
            creator=test_user,
            start_date=datetime(2025, 1, 1).date(),
            start_time=datetime(2025, 1, 1, 10),
            end_date=datetime(2025, 1, 1).date(),
            end_time=datetime(2025, 1, 1, 11),
        )

        Event.objects.create(
            title="Study Group",
            body="study",
            event_id="study",
            creator=test_user,
            start_date=datetime(2025, 1, 1).date(),
            start_time=datetime(2025, 1, 1, 10),
            end_date=datetime(2025, 1, 1).date(),
            end_time=datetime(2025, 1, 1, 11),
        )

        response = self.client.get("/events/?search=Soccer")
        self.assertContains(response, "Soccer Night")
        self.assertNotContains(response, "Study Group")
