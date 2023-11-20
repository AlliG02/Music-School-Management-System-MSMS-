"""Create user models that are to be used in the app """

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.core.validators import MinValueValidator
from datetime import datetime

class requestLesson(models.Model):

    INTERVAL_CHOICES = [
        (1, '1 Week'),
        (2, '2 Weeks'),
    ]
    DURATION_CHOICES = [
        (30, '30 Minutes'),
        (45, '45 Minutes'),
        (60, '1 Hour'),
    ]
    TEACHER_CHOICES = [
        ('Mr. Gough', 'Mr. Gough'),
        ('Mr. Mahendra', 'Mr. Mahendra'),
        ('Mr. Grebenyuk', 'Mr. Grebenyuk'),
        ('Mr. Thavaratnam', 'Mr. Thavaratnam'),
        ('Mr. Atta', 'Mr. Atta'),
    ]
    INSTRUMENT_CHOICES = [
        ('Piano','Piano'),
        ('Guitar','Guitar'),
        ('Drums','Drums'),
    ]
    date = models.DateField(default = None)

    time = models.TimeField(default = None)

    numberOfLessons = models.IntegerField(blank = False,
        validators=[MinValueValidator(0)]
    )
    intervalBetweenLessons = models.IntegerField(
        blank = False,
        choices = INTERVAL_CHOICES,
        default=INTERVAL_CHOICES[0],
    )

    duration = models.IntegerField(
        blank = False,
        choices = DURATION_CHOICES,
        default=DURATION_CHOICES[0],
    )
    teacher = models.CharField(
        max_length = 35,
        blank = False,
        choices = TEACHER_CHOICES,
        default=TEACHER_CHOICES[0],
    )
    instrument = models.CharField(
        max_length = 35,
        blank = False,
        choices = INSTRUMENT_CHOICES,
        default=INSTRUMENT_CHOICES[0],
    )


class Student(AbstractUser):
    #a limited selection of types of user of the app which will grow as app expands to parents, prevents error of semantics regarding precision of input for example Student or student
    ROLE_CHOICES = [
        ('Student','Student')
    ]

    role = models.CharField(
        max_length = 30,
        blank = False,
        choices = ROLE_CHOICES,
        default=ROLE_CHOICES[0],
    )

    username = models.EmailField(
        unique = True,
        blank = False,
        max_length = 50,
    )

    first_name = models.CharField(max_length = 15, blank = False)
    last_name = models.CharField(max_length = 15, blank = False)

