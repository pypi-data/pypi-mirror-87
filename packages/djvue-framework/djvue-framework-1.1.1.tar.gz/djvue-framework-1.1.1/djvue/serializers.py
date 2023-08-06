from enum import Enum

from django.urls import reverse
from django.utils.functional import cached_property
import rest_framework
from django.utils.encoding import force_str
from rest_framework import serializers
from rest_framework.fields import ChoiceField
from rest_framework.serializers import ModelSerializer


class DVSerializer:
    baseUrl = None
    dv_fields = []

    def get_dv_info(self):
        ret = {
            'listBaseUrl': reverse(self.baseUrl + '-list'),
            'detailBaseUrl': reverse(self.baseUrl + '-detail', kwargs={'pk': -1})
        }

        for i in self.dv_fields:
            value = getattr(self, i, None)
            if isinstance(value, Enum):
                value = value.value
            if value is not None and value != rest_framework.fields.empty:
                ret[i] = force_str(value, strings_only=True)
        return ret


class DVModelSerializer(ModelSerializer, DVSerializer):
    def __init__(self, baseUrl=None, *args, **kwargs):
        """

        :param baseUrl:
        :param args:
        :param kwargs:
        """
        super(DVModelSerializer, self).__init__(*args, **kwargs)
        self.baseUrl = baseUrl


class DjvueSerializerMixin:
    """
    Docstring for DjvueSerializerMixin
    """

    @cached_property
    def fields(self):
        fields = super().fields

        if hasattr(self, 'get_extra_buttons'):
            fields['extra_buttons'] = serializers.SerializerMethodField()

        return fields
