from django.urls import get_resolver

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, *args, **options):
        for key in set(v[1] for k,v in get_resolver(None).reverse_dict.items()):
          print(key)
