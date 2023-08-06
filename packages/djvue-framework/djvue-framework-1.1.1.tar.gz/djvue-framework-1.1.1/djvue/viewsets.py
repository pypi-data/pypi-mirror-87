from django.core.paginator import PageNotAnInteger, EmptyPage
from django.urls import reverse
from rest_framework.mixins import UpdateModelMixin, DestroyModelMixin, CreateModelMixin, RetrieveModelMixin, \
    ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.relations import ManyRelatedField
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.viewsets import GenericViewSet

from djvue.autocomplete import AutocompleteSerializer
from djvue.metadata import Metadata
from djvue.relations import DVAutocompletePrimaryKeyRelatedField
from djvue.serializers import DjvueSerializerMixin
from djvue.utils import ModalButton, ModalFormOperation
from django.utils.translation import gettext as _


class DjVuePagination(PageNumberPagination):
    def paginate_queryset(self, queryset, request, view=None):
        """
        Paginate a queryset if required, either returning a
        page object, or `None` if pagination is not configured for this view.
        The requested page number will be limited between the minimum and the maximum
        page number.
        """
        page_size = self.get_page_size(request)
        if not page_size:
            return None

        paginator = self.django_paginator_class(queryset, page_size)
        page_number = request.query_params.get(self.page_query_param, 1)
        if page_number in self.last_page_strings:
            page_number = paginator.num_pages

        try:
            self.page = paginator.page(page_number)
        except PageNotAnInteger:
            self.page = paginator.page(1)
        except EmptyPage:
            self.page = paginator.page(paginator.num_pages)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)


class DjVueGenericViewSet(GenericViewSet, ListModelMixin):
    """
    The DjVueGenericViewSet provide the base layer for DjVue interaction
    """

    list_fields = []
    search_fields = []
    ordering_fields = []
    list_select_key = ''
    metadata_class = Metadata
    tableProps = {}

    filter_backends = api_settings.DEFAULT_FILTER_BACKENDS
    ac_page_size = 10

    def get_ac_fields(self, view, request):
        model_class = self.autocomplete_field.queryset.model
        if hasattr(model_class, 'get_ac_search_field'):
            return model_class.get_ac_search_field()
        return ()

    def filter_ac_queryset(self, queryset):
        for backend in list(self.filter_backends):
            bk = backend()
            bk.get_search_fields = self.get_ac_fields
            queryset = bk.filter_queryset(self.request, queryset, self)
        return queryset

    def get_autocomplete_serializer_class(self):
        return AutocompleteSerializer

    def get_ac_field_queryset(self, field):
        return field.get_queryset()

    def get_autocomplete(self, request, *args, **kwargs):
        serializer = self.get_serializer()
        field = serializer.fields.get(request.GET.get('field'), None)
        pagination = int(request.GET.get('pagination', self.ac_page_size))

        if field.__class__ == ManyRelatedField:
            field = field.child_relation
        if field is not None and field.__class__ == DVAutocompletePrimaryKeyRelatedField:
            self.autocomplete_field = field
            serializer_class = self.get_autocomplete_serializer_class()

            q_ids = request.GET.get('ids', None)

            queryset = self.filter_ac_queryset(self.get_ac_field_queryset(field))

            ids_data = []
            if q_ids is not None and q_ids != '':
                id_filter = [int(v) for v in q_ids.split(',')]
                ids_qs = field.get_queryset().filter(id__in=id_filter)
                queryset = queryset.exclude(id__in=id_filter)
                ids_data = serializer_class(ids_qs, many=True).data

            if pagination > 0:
                queryset = queryset[:pagination]

            search_data = serializer_class(queryset, many=True)
            return Response(ids_data + search_data.data)

        return Response({'error': _('Unknown field for autocomplete')}, status=500)

    def allow_creation(self):
        return isinstance(self, CreateModelMixin)

    def allow_retrieve(self):
        return isinstance(self, RetrieveModelMixin)

    def allow_update(self):
        return isinstance(self, UpdateModelMixin)

    def allow_delete(self):
        return isinstance(self, DestroyModelMixin)

    def has_extra_buttons(self):
        return self.action == 'list'

    def has_footer(self):
        return hasattr(self, 'get_footer')

    def get_footer_config(self, view):
        return Response({'footer': self.get_footer()})

    def get_create_button(self):
        url_name = self.basename + '-list'
        if self.allow_creation():
            return ModalButton(key='dv_create', props={
                "baseUrl": reverse(url_name),
                "operation": ModalFormOperation.CREATE,
                "button_props": {
                    'label': '',
                    'class': 'p-1 ml-2 d-flex justify-content-center align-items-center',
                    'variant': 'success',
                }
            }).__dict__
        return None

    def get_extra_buttons(self, obj):
        """
        Returns the list of extra buttons
        """
        url_name = self.basename + '-detail'
        buttons = []

        if self.allow_retrieve():
            buttons.append(ModalButton(key='dv_detail', props={
                "baseUrl": reverse(url_name, kwargs={'pk': obj.id}),
                "operation": ModalFormOperation.DETAIL,
                "button_props": {
                    'label': '',
                    'class': 'p-1 ml-2 d-flex justify-content-center align-items-center',
                    'variant': 'primary'
                }
            }).__dict__)

        if self.allow_update():
            buttons.append(ModalButton(key='dv_update', props={
                "baseUrl": reverse(url_name, kwargs={'pk': obj.id}),
                "operation": ModalFormOperation.UPDATE,
                "button_props": {
                    'label': '',
                    'class': 'p-1 ml-2 d-flex justify-content-center align-items-center',
                    'variant': 'warning'
                }
            }).__dict__)

        if self.allow_delete():
            buttons.append(ModalButton(key='dv_delete', props={
                "baseUrl": reverse(url_name, kwargs={'pk': obj.id}),
                "operation": ModalFormOperation.DELETE,
                "button_props": {
                    'label': '',
                    'class': 'p-1 ml-2 d-flex justify-content-center align-items-center',
                    'variant': 'danger'
                }
            }).__dict__)

        return buttons

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer_class = self.get_serializer_class()
        data = self.get_serializer_context()

        if self.has_extra_buttons():
            data["get_extra_buttons"] = self.get_extra_buttons
            serializer_class = type(serializer_class.__name__, (DjvueSerializerMixin, serializer_class), data)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializer_class(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializer_class(queryset, many=True)
        return Response(serializer.data)

    def list_keys(self, request, *args, **kwargs):
        return Response(self.get_queryset().values_list(self.list_select_key, flat=True))
