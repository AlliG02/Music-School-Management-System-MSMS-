"""Configuration of the directors/admins interface for the management system"""
from django.contrib import admin
from .models import Student, requestLesson


@admin.register(Student)
class Admin(admin.ModelAdmin):
    list_display = [
        'username',
    ]



