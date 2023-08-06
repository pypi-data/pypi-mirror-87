from rest_framework.relations import PrimaryKeyRelatedField
from djvue.fields import DEFAULT_DV_FORM_SIZE, DVField


# Attenzione: nel caso in cui si tratti di una relazione many to many, le informazioni non vengono prese dal get_dv_info
# ma bensì inserite direttamente dalla classe metadata, questo a causa di un funzionamento interno di django drf


class DVAutocompletePrimaryKeyRelatedField(PrimaryKeyRelatedField, DVField):
    """
       Equivalent of DRF PrimaryKeyRelatedField
    """
    allow_creation = False
    placeholder = None
    widget = None
    ac = True

    def __init__(self, widget=None, placeholder=None, allow_creation=False, size=DEFAULT_DV_FORM_SIZE,
                 *args, **kwargs):
        """

        :param widget:
        :param placeholder:
        :param allow_creation:
        :param size:
        :param args:
        :param kwargs:
        """
        self.placeholder = placeholder
        self.allow_creation = allow_creation
        self.widget = widget
        self.size = size
        PrimaryKeyRelatedField.__init__(self, **kwargs)

    class Meta(DVField.Meta):
        dv_field = DVField.Meta.dv_field + ('ac', 'placeholder')


class DVInlinePrimaryKeyRelatedField(PrimaryKeyRelatedField, DVField):
    placeholder = None

    def __init__(self, placeholder=None,
                 *args, **kwargs):
        self.placeholder = placeholder
        PrimaryKeyRelatedField.__init__(self,many=True, **kwargs)