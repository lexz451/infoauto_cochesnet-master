from django.conf.urls import url
from django.urls import include
from rest_framework.routers import DefaultRouter

from infoauto.netelip.views import CallReceiverView, CallControlView


router = DefaultRouter()
router.register('call_control', CallReceiverView, base_name='call_control')
router.register('calls', CallControlView, base_name="calls")


urlpatterns = [
    url(r'^netelip/', include(router.urls)),
]
