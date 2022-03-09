from django.core.management.base import BaseCommand

from infoauto.netelip.utils import ubunet_calls


class Command(BaseCommand):
    help = "Descarga llamadas desde Ubunet"

    def handle(self, *args, **options):
        ubunet_calls()
