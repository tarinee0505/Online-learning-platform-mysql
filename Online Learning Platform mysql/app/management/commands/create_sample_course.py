from django.core.management.base import BaseCommand
from scripts.create_sample_course import create_sample_course

class Command(BaseCommand):
    help = 'Creates a sample course with modules'

    def handle(self, *args, **kwargs):
        course = create_sample_course()
        self.stdout.write(self.style.SUCCESS(f'Successfully created course "{course.title}"')) 