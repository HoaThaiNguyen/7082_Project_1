from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Group


class GroupTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='owner', password='pass123')

    def test_group_list_requires_login(self):
        response = self.client.get(reverse('group_list'))
        self.assertEqual(response.status_code, 302)  # redirect to login

    def test_group_list_loads_for_logged_in_user(self):
        self.client.login(username='owner', password='pass123')
        response = self.client.get(reverse('group_list'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'groups/group_list.html')

    def test_group_create(self):
        self.client.login(username='owner', password='pass123')

        response = self.client.post(reverse('group_create'), {
            'name': 'Test Group',
        })

        self.assertEqual(Group.objects.count(), 1)
        self.assertRedirects(response, reverse('group_list'))

    def test_group_detail(self):
        self.client.login(username='owner', password='pass123')

        group = Group.objects.create(name="G1", owner=self.user)

        response = self.client.get(reverse('group_detail', args=[group.id]))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "G1")
