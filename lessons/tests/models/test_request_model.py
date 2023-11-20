from django.test import TestCase
from lessons.models import requestLesson
from django.core.exceptions import ValidationError
from django.utils import timezone 

class RequestModelTestCase(TestCase):
    def setUp(self):
        self.request = requestLesson.objects.create(
            date = '2023-12-9',
            time = '10:00',
            numberOfLessons = 3,
            intervalBetweenLessons = 1,
            duration = 30,
            teacher = 'Mr. Gough',
            instrument = 'Drums'
        )

    #check if the model is valid
    def test_valid_request(self):
        self._assert_request_is_valid()

    #reject if the date is the current day 
    def test_reject_if_date_is_current_day(self):
        if self.request.date == '2023-12-8':
            self.assertFalse(self._assert_request_is_valid())
            self.fail('Date is invalid. Choose a date in the future')

    def _assert_request_is_valid(self):
        try:
            self.request.full_clean()
        except (ValidationError):
            self.fail("Request is not valid")