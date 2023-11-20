"""Tests for student model valid values"""
from django.test import TestCase
from lessons.models import Student
from django.core.exceptions import ValidationError

class StudentModelTestCase(TestCase):
    def setUp(self):
        self.student = Student.objects.create_user(
            'alexandergrebenyuk@msms.ac.uk',
            first_name = 'Alex',
            last_name = 'Greb',
            password = 'Password123',
            role = 'Student',
        )
    def test_valid_user(self):
        self._assert_student_is_valid()

    def test_username_cannot_be_blank(self):
        self.student.username = ''
        self._assert_student_is_invalid()

    def test_username_doesnt_allow_double_atsymbol(self):
        self.student.username = 'alexandergrebenyuk@@msms.ac.uk'
        self._assert_student_is_invalid()

    def test_username_is_unique(self):
        student = Student.objects.create_user(
            'alegre@msms.ac.uk',
            first_name = 'Ale',
            last_name = 'Gre',
            password = 'Password12',
            role = 'Student',
        )
        self.student.username = 'alegre@msms.ac.uk'
        self._assert_student_is_invalid()


    def test_username_is_not_over_limit(self):
        self.student.username = 'x' * 41 + 'msms.ac.uk'
        self._assert_student_is_invalid()

    def test_first_name_is_not_empty(self):
        self.student.first_name = ''
        self._assert_student_is_invalid()

    def test_first_name_is_over_limit(self):
        self.student.first_name = 'x' * 16
        self._assert_student_is_invalid()

    def test_first_name_is_not_over_limit(self):
        self.student.first_name = 'x' * 15
        self._assert_student_is_valid()

    def test_last_name_is_not_empty(self):
        self.student.last_name = ''
        self._assert_student_is_invalid()

    def test_last_name_is_not_over_limit(self):
        self.student.last_name = 'x' * 16
        self._assert_student_is_invalid()

    def test_last_name_is_not_over_limit(self):
        self.student.last_name = 'x' * 15
        self._assert_student_is_valid()

    def test_role_is_not_empty(self):
        self.student.role = ''
        self._assert_student_is_invalid()

    #tests for role to be changed as selection should only be chosen from child/student and parent/student
    #length test is redundant as only accepts from role choices list
    def test_role_is_under_limit(self):
        self.student.role = 'x' * 31
        self._assert_student_is_invalid()

    def test_role_is_under_limit(self):
        self.student.role = 'x' * 29
        self._assert_student_is_invalid()

    def test_role_is_student(self):
        self.student.role = 'Student'
        self._assert_student_is_valid()


    def _assert_student_is_valid(self):
        try:
            self.student.full_clean()
        except (ValidationError):
            self.fail("Test student should be valid")

    def _assert_student_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.student.full_clean()
