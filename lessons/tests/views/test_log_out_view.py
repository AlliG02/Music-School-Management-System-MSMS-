"""Create tests for when a user logs out"""
from django.test import TestCase
from django.urls import reverse
from lessons.models import Student
from lessons.tests.helpers import LogInTester

class LogOutTest(TestCase, LogInTester):
    def setUp(self):
        self.url = reverse('log_out')
        self.student = Student.objects.create_user(
            'alexandergrebenyuk@msms.ac.uk',
            first_name = 'Alex',
            last_name = 'Greb',
            password = 'Password123',
            role = 'Student',
        )
    def test_log_out_url(self):
        self.assertEqual(self.url, '/log_out/')

    def test_get_log_out(self):
        self.client.login(username = 'alexandergrebenyuk@msms.ac.uk', password = 'Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow = True)
        response_url = reverse('greet')
        self.assertRedirects(response, response_url, status_code = 302, target_status_code = 200)
        self.assertTemplateUsed(response, 'greet.html')
        self.assertFalse(self._is_logged_in())
