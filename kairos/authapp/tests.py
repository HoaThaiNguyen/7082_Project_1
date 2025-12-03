from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User


class AuthAppTests(TestCase):

    def test_signup_creates_user_and_redirects(self):
        response = self.client.post(reverse('signup'), {
            'username': 'testuser',
            'password1': 'StrongPass123!',
            'password2': 'StrongPass123!',
        })

        self.assertEqual(User.objects.count(), 1)
        self.assertRedirects(response, reverse('events:list'))

    def test_login_valid_user(self):
        user = User.objects.create_user(username='test', password='pass12345')

        response = self.client.post(reverse('login'), {
            'username': 'test',
            'password': 'pass12345'
        })

        # Should redirect to /events
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/events')

    def test_logout_redirects_to_login(self):
        user = User.objects.create_user(username='test', password='pass12345')
        self.client.login(username='test', password='pass12345')

        response = self.client.get(reverse('logout'))

        self.assertRedirects(response, reverse('login'))
