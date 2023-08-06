from collections import OrderedDict

import rest_framework
from rest_framework.fields import empty, ListField
from rest_framework.metadata import BaseMetadata
from rest_framework.request import clone_request

from django.utils.encoding import force_str

from rest_framework import exceptions, serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.utils.field_mapping import ClassLookupDict

from djvue.fields import DVField
from djvue.serializers import DVSerializer, DVModelSerializer

attrs = [
    'read_only', 'label', 'help_text',
    'min_length', 'max_length',
    'min_value', 'max_value', 'default'
]


class Metadata(BaseMetadata):
    """
    This is the default metadata implementation.
    It returns an ad-hoc set of information about the view.
    There are not any formalized standards for `OPTIONS` responses
    for us to base this on.
    """
    label_lookup = ClassLookupDict({
        serializers.Field: 'field',
        serializers.BooleanField: 'boolean',
        serializers.NullBooleanField: 'boolean',
        serializers.CharField: 'string',
        serializers.UUIDField: 'string',
        serializers.URLField: 'url',
        serializers.EmailField: 'email',
        serializers.RegexField: 'regex',
        serializers.SlugField: 'slug',
        serializers.IntegerField: 'integer',
        serializers.FloatField: 'float',
        serializers.DecimalField: 'decimal',
        serializers.DateField: 'date',
        serializers.DateTimeField: 'datetime',
        serializers.TimeField: 'time',
        serializers.ChoiceField: 'choice',
        serializers.MultipleChoiceField: 'multiple choice',
        serializers.FileField: 'file upload',
        serializers.ImageField: 'image upload',
        serializers.ListField: 'list',
        serializers.DictField: 'nested object',
        serializers.Serializer: 'nested object',
    })

    @staticmethod
    def set_action_from_method(view, method):
        m = method.lower()
        view.action = view.action_map.get(m)

    def get_extended_serializer_info(self, serializer, view):
        # todo dare la possibilita, a partire dalla view di poter specificare dei metodi o delle proprieta per prendere
        # delle informazioni estra sui campi, per esempio per poter pasare le proprieta alle colonne del front
        return {
            'fields': self.get_serializer_info(serializer),
            'form': serializer.get_form_layout() if hasattr(serializer, 'get_form_layout') else None
        }

    def determine_metadata(self, request, view):
        metadata = OrderedDict()
        metadata['name'] = view.get_view_name()
        metadata['description'] = view.get_view_description()
        metadata['renders'] = [renderer.media_type for renderer in view.renderer_classes]
        metadata['parses'] = [parser.media_type for parser in view.parser_classes]
        if hasattr(view, 'get_serializer'):
            actions = self.determine_actions(request, view)
            if actions:
                metadata['actions'] = actions
        return metadata

    def determine_actions(self, request, view):

        actions = {}
        for method in [m for m in view.allowed_methods if m.lower() not in ['head', 'options', 'trace']]:
            view.request = clone_request(request, method)

            self.set_action_from_method(view, method)

            serializer = view.get_serializer()
            actions[method] = self.get_extended_serializer_info(serializer, view)
            if method == 'GET':
                actions[method].update(self.get_list_info(request, view))
            view.request = request

        return actions

    def get_serializer_info(self, serializer):
        """
        Given an instance of a serializer, return a dictionary of metadata
        about its fields.
        """
        if hasattr(serializer, 'child'):
            # If this is a `ListSerializer` then we want to examine the
            # underlying child serializer instance instead.
            serializer = serializer.child
        return OrderedDict([
            (field_name, self.get_field_info(field))
            for field_name, field in serializer.fields.items()
            if not isinstance(field, serializers.HiddenField)
        ])

    @staticmethod
    def get_default_drf_info(field):
        ret = {}
        for attr in attrs:
            value = getattr(field, attr, None)
            if value is not None and value != rest_framework.fields.empty:
                ret[attr] = force_str(value, strings_only=True)
        return ret

    def get_field_info(self, field):
        """
        Given an instance of a serializer field, return a dictionary
        of metadata about it.
        """
        field_info = OrderedDict()
        field_info['type'] = self.label_lookup[field]
        field_info['name'] = field.field_name
        field_info['required'] = getattr(field, 'required', False)

        if isinstance(field, serializers.ManyRelatedField) and isinstance(field.child_relation, DVField):
            field_info = {**field_info, **field.child_relation.get_dv_info(), 'label': getattr(field, 'label', None),
                          'many': True}
        elif isinstance(field, DVField):
            field_info = {**field_info, **field.get_dv_info()}
        else:
            field_info = {**field_info, **self.get_default_drf_info(field)}

        if getattr(field, 'child', None):
            if isinstance(field.child, DVModelSerializer):
                field_info['model'] = field.child.get_dv_info()
            field_info['type'] = 'nested object'

        # elif getattr(field, 'fields', None):
        #     field_info['children'] = self.get_serializer_info(field)

        # if (not field_info.get('read_only') and
        #     not isinstance(field, (serializers.RelatedField, serializers.ManyRelatedField)) and
        #         hasattr(field, 'choices')):
        #     field_info['choices'] = [
        #         {
        #             'id': choice_value,
        #             'text': force_str(choice_name, strings_only=True)
        #         }
        #         for choice_value, choice_name in field.choices.items()
        #     ]

        return field_info

    @staticmethod
    def get_list_info(request, view):

        metadata = {
            'is_paginated': False,
            'page_size': None,
            'search_filter': {
                'search_fields': [], 'search_param': ''
            },
            'ordering_filter': {
                'ordering_fields': [], 'ordering_param': ''
            },
            'has_footer': view.has_footer(),
            'list_fields': view.list_fields,
            'list_select_key': view.list_select_key,
            'has_extra_buttons': view.has_extra_buttons(),
            'allow_creation': view.allow_creation(),
            'create_button': view.get_create_button()
        }

        if view.paginator:
            metadata['is_paginated'] = True
            metadata['page_size'] = view.paginator.page_size
            metadata['page_param'] = view.paginator.page_query_param

        for filter in view.filter_backends:

            if hasattr(filter, 'search_param'):
                metadata['search_filter'] = {
                    'search_fields': view.search_fields,
                    'search_param': filter.search_param
                }
            if hasattr(filter, 'ordering_param'):
                metadata['ordering_filter'] = {
                    'ordering_fields': view.ordering_fields,
                    'ordering_param': filter.ordering_param
                }

        return metadata
