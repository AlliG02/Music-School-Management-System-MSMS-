"""Tests the form that the user uses to create a request for a lesson"""
from django.test import TestCase
from django import forms
from lessons.forms import requestLessonForm

class requestLessonForm(TestCase):

    def setUp(self):
        self.form_data ={
            'date' : '12/12/2023',
            'time' : '10:00',
            'numberOfLessons' : 1,
            'intervalBetweenLessons' : 1,
            'duration' :30 ,
            'teacher' : 'Mr. Gough',
            'instrument' : 'Piano'
        }

    def test_accept_form_with_valid_input(self):
        form = requestLessonForm(data = self.form_data)
        self.assertTrue(form.is_valid())

    def test_rejects_date_value_prior_to_current_day(self):
        form = requestLessonForm(data = self.form_data)
        self.form_data['date'] = '12/12/2020'
        self.assertFalse(form.is_valid())
            
    def test_rejects_empty_number_of_lessons(self): 
        form = requestLessonForm(data = self.form_data)
        self.form_data['numberOfLessons'] = ''
        self.assertFalse(form.is_valid())

    def test_rejects_number_of_lessons_equal_0(self):
        form = requestLessonForm(data = self.form_data)
        self.form_data['numberOfLessons'] = 0
        self.assertFalse(form.is_valid())
