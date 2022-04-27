from django.db.models.signals import pre_save

from infoauto.common.signals import set_old_instance
from infoauto.leads.models.leads import LeadAction, Lead
from infoauto.leads.signals.leadactions import set_status
from infoauto.leads.signals.leads import lead_callback
from infoauto.leads.signals.tasks import task_callback

pre_save.connect(set_old_instance, sender=Lead)
pre_save.connect(set_old_instance, sender=LeadAction)
