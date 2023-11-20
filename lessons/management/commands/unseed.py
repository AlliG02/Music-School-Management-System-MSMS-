from django.core.management.base import BaseCommand, CommandError
from lessons.models import Student, requestLesson

class Command(BaseCommand):
    def handle(self, *args, **options):
        Student.objects.filter(is_staff=False, is_superuser=False).delete()
        requestLesson.objects.filter().delete()
