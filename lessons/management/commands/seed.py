from django.core.management.base import BaseCommand, CommandError
from faker import Faker
from lessons.models import Student

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.faker = Faker('en_GB')

    def handle(self, *args, **options):
        print("The seed command has not been implemented yet!")
        print("TO DO: Create a seed command following the instructions of the assignment carefully.")
