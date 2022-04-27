from django.core.management.base import BaseCommand
from infoauto.netelip.utils import check_calls


class Command(BaseCommand):
    help = "Auto assign call"

    def handle(self, *args, **options):
        check_calls()
