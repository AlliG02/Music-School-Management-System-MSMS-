"""Unit tests for the sign up form"""
from django.test import TestCase
from lessons.models import Student
from django.core.exceptions import ValidationError
from lessons.forms import SignUpForm
from django import forms
from django.contrib.auth.hashers import check_password

class StudentModelTestCase(TestCase):
    #Form accepts valid data
    def setUp(self):
        self.form_data = {
            'username':'alexg@msms.ac.uk',
            'first_name':'Alex',
            'last_name':'G',
            'role':'Student',
            'password':'Password123',
            'password_confirmation':'Password123',
        }

    def test_valid_data(self):
        form = SignUpForm(data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_has_intended_fields(self):
        form = SignUpForm()
        self.assertIn('username', form.fields)
        username_field =form.fields['username']
        self.assertTrue(isinstance(username_field, forms.EmailField))
        self.assertIn('last_name', form.fields)
        self.assertIn('first_name', form.fields)
        self.assertIn('role', form.fields)
        self.assertIn('password', form.fields)
        password_widget = form.fields['password'].widget
        self.assertTrue(isinstance(password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_form_uses_model_validation(self):
        self.form_data['username'] = 'alexg@msms'
        form = SignUpForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_password_requires_number(self):
        self.form_data['password_confirmation'] = 'Password'
        form = SignUpForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_password_requires_capital_letter(self):
        self.form_data['password_confirmation'] = 'password1234'
        form = SignUpForm(data=self.form_data)
        self.assertFalse(form.is_valid())

    def test_passwords_equal(self):
        self.form_data['password_confirmation'] = 'Password1234'
        form = SignUpForm(data=self.form_data)
        self.assertFalse(form.is_valid())


    def test_form_must_save(self):
        form = SignUpForm(data=self.form_data)
        before_count_objects = Student.objects.count()
        form.save()
        after_count_objects = Student.objects.count()
        self.assertEqual(after_count_objects, before_count_objects + 1)
        student = Student.objects.get(username = 'alexg@msms.ac.uk')
        self.assertEqual(student.first_name,'Alex')
        self.assertEqual(student.last_name,'G')
        self.assertEqual(student.role,'Student')
        correct_password = check_password('Password123', student.password)
        self.assertTrue(correct_password)
