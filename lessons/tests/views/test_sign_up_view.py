"""Create tests for sign up functionality """
from django.test import TestCase
from lessons.forms import SignUpForm
from django.urls import reverse
from lessons.models import Student
from django.contrib.auth.hashers import check_password
from lessons.tests.helpers import LogInTester

class SignUpView(TestCase, LogInTester):

    def setUp(self):
        self.url = reverse('sign_up')
        self.form_data = {
            'username':'alexg@msms.ac.uk',
            'first_name':'Alex',
            'last_name':'G',
            'role':'Student',
            'password':'Password123',
            'password_confirmation':'Password123',
        }

    def test_get_sign_up_url(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_wrong_data(self):
        self.form_data['username'] = 'al@@msms.ac.uk'
        before_count_objects = Student.objects.count()
        response = self.client.post(self.url, self.form_data)
        after_count_objects = Student.objects.count()
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sign_up.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertEqual(after_count_objects, before_count_objects)
        self.assertFalse(self._is_logged_in())


    def test_success_redirect(self):
        response = self.client.post(self.url, self.form_data, follow=True)
        response_url = reverse('home')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertTrue(self._is_logged_in())


    def test_success_student_object_creation(self):
        before_count_objects = Student.objects.count()
        response = self.client.post(self.url, self.form_data, follow=True)
        after_count_objects = Student.objects.count()
        self.assertEqual(after_count_objects, before_count_objects + 1)
        student = Student.objects.get(username = 'alexg@msms.ac.uk')
        self.assertEqual(student.first_name,'Alex')
        self.assertEqual(student.last_name,'G')
        self.assertEqual(student.role,'Student')
        correct_password = check_password('Password123', student.password)
        self.assertTrue(correct_password)
        self.assertTrue(self._is_logged_in())

