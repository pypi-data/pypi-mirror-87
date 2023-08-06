from django.core.management.base import BaseCommand
from django.db import connection

from django_postgres_matviews.utils import get_matviews


class Command(BaseCommand):

    def handle(self, *args, **options):
        matviews = get_matviews()
        if matviews:
            print("\n".join(matviews))
