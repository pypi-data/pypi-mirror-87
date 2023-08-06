from rest_framework import serializers


class AutocompleteSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.SerializerMethodField()

    def get_text(self, obj):
        return str(obj)


class AutocompleteProdottoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    text = serializers.CharField(source='descrizione')

    def get_text(self, obj):
        return str(obj)
