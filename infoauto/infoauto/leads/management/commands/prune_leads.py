from django.core.management.base import BaseCommand
from infoauto.leads.models import Task, Lead

class Command(BaseCommand):
    help = "Prune some lead, related to concessionaire"

    def handle(self, *args, **options):
        queryset = Lead.objects.filter(concessionaire__in=[47, 4, 12, 13])
        count = queryset.count()
        queryset.delete()
        description = "Borrados con éxito, {} leads".format(count)
        self.stdout.write(self.style.SUCCESS(description))