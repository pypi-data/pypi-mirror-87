from django.core.management.base import BaseCommand
from django.db import connection

from django_postgres_matviews.utils import drop_matviews


class Command(BaseCommand):

    def handle(self, *args, **options):
        drop_matviews()
