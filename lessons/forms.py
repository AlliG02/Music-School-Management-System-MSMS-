""" Create forms and methods for a form for a user of the app to use"""
from django import forms
from .models import Student, requestLesson
from django.core.validators import RegexValidator
import datetime


class requestLessonForm(forms.ModelForm):
    class Meta:
        
        class DateInput(forms.DateInput):
            input_type = 'date'

        class TimeInput(forms.DateInput):
            input_type = 'time'

        model = requestLesson
        fields = ['date', 'time', 'numberOfLessons', 'intervalBetweenLessons', 'duration', 'teacher', 'instrument']
        widgets = {
            'date': DateInput(),
            'time': TimeInput(),
        }
    numberOfLessons = forms.IntegerField(label = "Number Of Lessons")

    def clean_date(self):
        date = self.cleaned_data['date']
        if date <= datetime.date.today():
            raise forms.ValidationError("You can only book a lesson for tomorrow onwards!")
        return date

class LogInForm(forms.Form):
    username = forms.EmailField(label = "Email")
    password = forms.CharField(label = "Password", widget = forms.PasswordInput)

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['username', 'first_name', 'last_name', 'role']

    #add requirements with messages here for sign up form fields to ensure user can correct their field data input
    username = forms.EmailField(
        label = 'Email',
    )
    password = forms.CharField(
        label = 'Password',
        widget = forms.PasswordInput(),
        validators = [RegexValidator(
            regex = r'^(?=.*[A-Z])(?=.*[0-9]).*$',
            message = 'Your password requires a capital letter with a number',
        )]
    )

    password_confirmation = forms.CharField(label = 'Password Confirmation', widget = forms.PasswordInput())

    #override clean method to ensure all fields in the sign up form can be validated
    def clean(self):
        super().clean()
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            self.add_error('password_confirmation', 'Passwords do not match!')

    #override save function to ensure the addition of an object has its password hashed
    def save(self):
        super().save(commit=False)
        student = Student.objects.create_user(
            self.cleaned_data.get('username'),
            first_name = self.cleaned_data.get('first_name'),
            last_name = self.cleaned_data.get('last_name'),
            role = self.cleaned_data.get('role'),
            password = self.cleaned_data.get('password'),
        )
        return student
