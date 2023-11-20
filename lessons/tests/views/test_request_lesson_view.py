"""Create tests for create request functionality """
from django.test import TestCase
from lessons.forms import SignUpForm
from django.urls import reverse
from lessons.models import requestLesson

class RequestLessonView(TestCase):

    def setUp(self):
        self.url = reverse('requestLesson')
        self.form_data = {
            'date' : '12/12/2023',
            'time' : '10:00',
            'numberOfLessons' : 1,
            'intervalBetweenLessons' : 1,
            'duration' :30 ,
            'teacher' : 'Mr. Gough',
            'instrument' : 'Piano'
         }

    def test_request_lesson_view(self):
        self.assertEqual(self.url, '/requestLesson/')
