# -*- coding: utf-8 -*-

from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from infoauto.netelip_leads.views import CallControlView, CallControlLeadView, CallReceiverView, CallHistoryView

router = DefaultRouter()
router.register('call_control_lead', CallControlLeadView, base_name='call_control_lead')
router.register('call_manager', CallControlView, base_name="call_manager")
router.register('_calls_', CallReceiverView, base_name="_calls_")
router2 = DefaultRouter()
router2.register('historic', CallHistoryView, base_name="historic")

urlpatterns = [
    url(r'^netelip/', include(router.urls)),
    url(r'lead-', include(router2.urls))
]
