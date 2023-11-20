"""Tests the log in functionality"""
from django.test import TestCase
from lessons.forms import LogInForm
from django.urls import reverse
from lessons.models import Student
from lessons.tests.helpers import LogInTester
from django.contrib import messages
class LogInView(TestCase, LogInTester):

    def setUp(self):
        self.url = reverse('log_in')
        self.student = Student.objects.create_user(
            'alexg@msms.ac.uk',
            first_name = 'Alex',
            last_name = 'Greb',
            password = 'Password123',
            role = 'Student',
        )

    def test_log_in_url(self):
        self.assertEqual(self.url, '/log_in/')

    def test_get_log_in_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)

    def test_unsuccessful_log_in(self):
        form_data = {'username':'alexg@msms.ac.uk', 'password':'Password12'}
        response = self.client.post(self.url, form_data, follow = True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'log_in.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 1)
        self.assertEqual(messages_list[0].level, messages.ERROR)

    def test_successful_log_in(self):
        form_data = {'username':'alexg@msms.ac.uk', 'password':'Password123'}
        response = self.client.post(self.url, form_data, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue(self._is_logged_in())
        messages_list = list(response.context['messages'])
        self.assertEqual(len(messages_list), 0)
