from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from notifications.models import Notification
from datetime import datetime


class CreateEventTests(TestCase):

    def setUp(self):
        self.fromUser = User.objects.create_user(username="m", password="1234")
        self.toUser = User.objects.create_user(username="c", password="5678")
        self.toOtherUser = User.objects.create_user(username="o", password="3737")
        #self.client.login(username="m", password="1234")
        self.client.login(username="c", password="5678")
        #self.client.login(username="o", password="3737")

        # create test notifications
        self.n1 = Notification.objects.create(
            from_user=self.fromUser,
            to_user=self.toUser,
            title="Event Deleted",
            description="Event you were a part of was deleted",
            url="/events"
        )

        self.n2 = Notification.objects.create(
            from_user=self.fromUser,
            to_user=self.toUser,
            title="Event Updated",
            description="Participant changed their status in an event you are a part of",
            url="/events/1"
        )

        self.nOtherUser = Notification.objects.create(
            from_user=self.fromUser,
            to_user=self.toOtherUser,
            title="Other Notification",
            description="Should not be seen when testing get notifications for toUser",
            url="/events/2"
        )

    def test_get_notifications(self):
        response = self.client.get(reverse("notifications:get_notifications"))
        notifications = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(notifications), 2)
        for notification in notifications:
            self.assertNotIn(notification["title"], "Other Notification")


    def test_mark_read(self):
        response = self.client.post(reverse("notifications:mark_notification_read", kwargs={"notification_id": self.n1.id}))
        self.n1.refresh_from_db()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.n1.is_read, True)
