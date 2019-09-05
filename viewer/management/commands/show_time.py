from django.core.management.base import BaseCommand
from django.utils import timezone


class Command(BaseCommand):
    help = 'loads in custom magical items for testing'

    def handle(self, *args, **options):
        time = timezone.now().strftime('%X')
        self.stdout.write("It's now %s" % time)
