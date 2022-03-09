from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.utils.translation import ugettext_lazy as _
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from infoauto.business_activity.views import BusinessActivityView, BusinessSectorView
from infoauto.chrome_extension.views import chrome_extension_update
from infoauto.click2call.views import Click2CallView
from infoauto.clients.views import ClientView
from infoauto.concessionaires.views import UserConcessionView, PhoneView, ConcessionaireView, EmailView, \
    ConcessionDashboardEmail
from infoauto.infodata_client.views import InfodataIncomingCallView
from infoauto.leads.views import LeadView, TaskView, GasTypeView, LeadCols, ACDView, OriginView, LeadFullHistoryView, \
    LeadActionView, LeadCalendarView, LeadImporterView, LeadWhastAppMessageView
from infoauto.leads_public.views import PublicLeadView
from infoauto.source_channels.views import ChannelView, SourceView
from infoauto.users.views import AuthenticationView, UserView, HistoricalSessionWithHistoricView, SFAView
from infoauto.countries.views_rest import Countries, Provinces, Localities
from infoauto.vehicles.views import VehicleView, AppraisalView, VehicleModelView, VehicleVersionView, VehicleBrandView
from infoauto.zadarma_client.views import IncomingCallZadarmaView

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   validators=['flex', 'ssv'],
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'business_activity', BusinessActivityView, base_name='business_activity')
router.register(r'business_sector', BusinessSectorView, base_name='business_activity')
router.register(r'lead', LeadView, base_name=_('Lead'))
router.register(r'auth', AuthenticationView, base_name=_('Auth'))
router.register(r'user', UserView, base_name=_('User'))
router.register(r'sfa', SFAView, base_name=_('SPA'))
router.register(r'concessionaire', ConcessionaireView, base_name=_('Concessionaire'))
router.register(r'task', TaskView, base_name=_('Task'))
router.register(r'countries', Countries, base_name=_('Countries'))
router.register(r'provinces', Provinces, base_name=_('Provinces'))
router.register(r'localities', Localities, base_name=_('Localities'))
router.register(r'gas_type', GasTypeView, base_name=_("Gas Type"))
router.register(r'lead_col', LeadCols, base_name=_("LeadCols"))
router.register(r'lead_calendar', LeadCalendarView, base_name=_("LeadCalendar"))
router.register(r'origin', OriginView, base_name=_("Origen"))
router.register(r'incoming_call', IncomingCallZadarmaView, base_name=_("Llamadas entrantes"))
router.register(r'incoming_call_infodata', InfodataIncomingCallView, base_name=_("Llamadas entrantes Infodata"))
router.register(r'acd', ACDView, base_name=_("ACDV"))
router.register(r'user_concession', UserConcessionView, base_name=_("Relación Usuario & Concesionario"))
router.register(r'phone', PhoneView, base_name=_("Teléfonos de concesionarios"))
router.register(r'email', EmailView, base_name=_("Emails de concesionarios"))
router.register(r'public-lead', PublicLeadView, base_name=_("API Pública de Leads"))
router.register(r'concession-dashboard', ConcessionDashboardEmail, base_name=_("Dashboard de Concesionarios"))
router.register(r'clients', ClientView, base_name=_("Clientes"))
router.register(r'channel', ChannelView, base_name=_("Canal"))
router.register(r'source', SourceView, base_name=_("Fuente"))
router.register(r'session_historic', HistoricalSessionWithHistoricView, base_name=_("Historico de Sesiones"))
router.register(r'click2call', Click2CallView, base_name=_("Click to call"))
router.register(r'lead_history', LeadFullHistoryView, base_name=_("Full Lead History"))
router.register(r'lead_actions', LeadActionView, base_name='lead_action')
router.register(r'vehicles', VehicleView, base_name='vehicles')
router.register(r'vehicles_model', VehicleModelView, base_name='vehicles_model')
router.register(r'vehicles_version', VehicleVersionView, base_name='vehicles_version')
router.register(r'vehicles_brand', VehicleBrandView, base_name='vehicles_brand')
router.register(r'appraisal', AppraisalView, base_name='appraisal')
router.register(r'lead_importer', LeadImporterView, base_name='lead_importer')
router.register(r'lead_whatsapp_message', LeadWhastAppMessageView, base_name='lead_whatsapp_message')


urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api/', include('infoauto.netelip.urls')),
    url(r'^api/', include('infoauto.netelip_leads.urls')),
    url(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0),
        name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(
        "about/",
        TemplateView.as_view(template_name="pages/about.html"),
        name="about",
    ),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path(
        "users/",
        include("infoauto.users.urls", namespace="users"),
    ),
    path(
        "chrome_extension_update/",
        chrome_extension_update, name="chrome_extension"
    ),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
