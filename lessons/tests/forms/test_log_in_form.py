"""Tests the form that the user uses to log in"""
from django.test import TestCase
from django import forms
from lessons.forms import LogInForm

class LogInFormTest(TestCase):

    def setUp(self):
        self.form_data = {'username':'alexg@msms.ac.uk', 'password':'Password!'}

    def test_form_contains_user_pass_field(self):
        form = LogInForm()
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
        password_field = form.fields['password']
        self.assertTrue(isinstance(password_field.widget, forms.PasswordInput))

    def test_form_accepts_valid_input(self):
        form = LogInForm(data = self.form_data)
        self.assertTrue(form.is_valid())

    def test_form_rejects_blank_username(self):
        self.form_data['username'] = ''
        form = LogInForm(data = self.form_data)
        self.assertFalse(form.is_valid())

    def test_form_rejects_blank_password(self):
        self.form_data['password'] = ''
        form = LogInForm(data = self.form_data)
        self.assertFalse(form.is_valid())
