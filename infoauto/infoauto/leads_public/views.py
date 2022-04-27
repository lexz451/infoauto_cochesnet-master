from django.conf import settings
from django.db.models import Q
from rest_condition import Or
from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_xml.parsers import XMLParser
from rest_framework_xml.renderers import XMLRenderer
from six import StringIO

from infoauto.common.permissions import IsAdminUser
from infoauto.common.util_email import send_email
from infoauto.leads.models import Lead, Concessionaire, UserConcession
from infoauto.leads.serializers import LeadSerializer
from infoauto.leads_public.permissions import IsAllowedToken
from infoauto.leads_public.serializers import PublicLeadSerializer


class PublicLeadRenderer(XMLRenderer):
    # item_tag_name = 'contacto'
    root_tag_name = 'callcenter'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Renders `data` into serialized XML.
        """
        if data is None:
            return ''

        stream = StringIO()

        from django.utils.xmlutils import SimplerXMLGenerator
        xml = SimplerXMLGenerator(stream, self.charset)
        xml.startDocument()
        xml.startElement(self.root_tag_name, {})
        self._to_xml(xml, data)
        xml.endElement(self.root_tag_name)
        xml.endDocument()
        return stream.getvalue()

    def _to_xml(self, xml, data):
        if isinstance(data, (list, tuple)):
            for item in data:
                # xml.startElement(self.item_tag_name, {})
                self._to_xml(xml, item)
                # xml.endElement(self.item_tag_name)

        elif isinstance(data, dict):
            import six
            for key, value in six.iteritems(data):
                xml.startElement(key, {})
                self._to_xml(xml, value)
                xml.endElement(key)

        elif data is None:
            # Don't output any value
            pass

        else:
            from django.utils.encoding import smart_text
            xml.characters(smart_text(data))


class LeadMapper(object):
    def _clean_empty_values(self, data):
        for i, j in data.items():
            if type(j) == dict:
                self._clean_empty_values(j)
            elif type(j) == list:
                data[i] = [elem.replace('\n', '').strip() if hasattr(elem, 'replace') else elem for elem in j]
            else:
                data[i] = j.replace('\n', '').strip() if hasattr(j, 'replace') else j

    @staticmethod
    def _get_tasks(coches):
        data = []
        coches = [coches] if type(coches) != list else coches
        for i in coches:
            data.append(
                {
                    'appraisal': {
                        'brand_model': "%s %s" % (
                            i['marca'],
                            i['modelo']
                        ),
                        'km': i['km'],
                        'license_plate': i['matricula'],
                        'year': i['fechaprimeramatriculacion']['anio']
                    },
                    'type': 'appraisal'
                }
            )
        return data

    @staticmethod
    def _get_notes(notes):
        data = []
        if type(notes) == list:
            [data.append({'content': i['comentario']}) for i in notes]
        else:
            data = [{'content': notes['comentario']}]
        return data

    @staticmethod
    def _get_concession_phone( nombre):
        try:
            phone = Concessionaire.objects.get(name=nombre).phones.all().first().number
        except Exception:
            phone = None
        return phone

    def manage_data(self, raw_data):
        self._clean_empty_values(raw_data)
        data = {}
        raw_data = [raw_data['contacto']] if type(raw_data['contacto']) != list else raw_data['contacto']
        for raw in raw_data:
            data.update({
                'client': {
                    'name': raw['nombre'],
                    'email': raw['email']
                },
                'request': {
                    'task': self._get_tasks(raw['tasacion']['coche'])
                },
                'vehicle': {
                    'brand_model': raw['interesado']['coche']['marca'],
                    'price': raw['interesado']['coche']['precio'],
                    'km': raw['interesado']['coche']['rangos']['kilometros']['hasta']
                },
                'note': self._get_notes(raw['notas']['anotacion']),
                'concession_phone': self._get_concession_phone(raw['concesiondestino'])
            })
        return data


class PublicLeadView(mixins.RetrieveModelMixin, mixins.ListModelMixin, mixins.CreateModelMixin, GenericViewSet,
                     LeadMapper):
    renderer_classes = (PublicLeadRenderer, )
    parser_classes = (XMLParser, )
    pagination_class = None
    serializer_class = PublicLeadSerializer
    queryset = Lead.objects.all().order_by("id")
    permission_classes = [Or(IsAdminUser, IsAllowedToken)]
    filter_fields = {'modified': ['gte']}
    search_fields = ('status', 'vehicle__brand_model', 'client__name', 'client__phone', 'request__task__description',
                     'request__task__realization_date', 'request__task__realization_date')

    def get_queryset(self):
        if self.request.user.is_authenticated and not self.request.user.is_admin:
            concessions = UserConcession.objects.filter(Q(is_concessionaire_admin=True) | Q(is_business_manager=True),
                                                        user=self.request.user).values_list('concessionaire', flat=True)
            self.queryset = self.queryset.filter(concessionaire__in=concessions)
        elif not self.request.user.is_authenticated:
            self.queryset = self.queryset.none()
        return super().get_queryset()

    def perform_create(self, serializer):
        super().perform_create(serializer)
        self.kwargs['pk'] = serializer.instance.id

    def create(self, request, *args, **kwargs):
        """
        TODO: real function to complete
        self.serializer_class = LeadSerializer
        data = self.manage_data(request.data)
        request.data.pop('contacto', None)
        request.data.update(data)
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            self.serializer_class = PublicLeadSerializer
            return super().retrieve(request, *args, **kwargs)
        else:
            return response
        """
        try:
            to_email = getattr(settings, 'MAIL_PUBLIC_RESPONSE', 'vomotorscoring@info-auto.es')
            send_email(to_email=[to_email],
                       subject="NUEVO LEAD DURSAN",
                       template='email/dursan_xml_content', context={'data': request.data}, request=request,
                       smtp_config_name="default")
            return Response("OK")
        except Exception as e:
            return Response("ERROR: %s" % str(e), status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({'contacto': serializer.data})

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response([{'contacto': i} for i in serializer.data])
