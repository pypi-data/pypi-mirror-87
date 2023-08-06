***********************
DjVue Serializer Fields
***********************

DjVue Serializer field are intended to use the functionality offered by DjVue Form and automatic form render.
These classes give a simplified way to communicate information about form from backend to frontend and can be used
to replace DjangoRestFramework serializer's fields.

Every **DjVue** serializer field is named like a **DRF** serializer field preceded by 'DV',
they accept every DRF field parameters plus **DjVue** extras. Refer to **DRF** fields documetation page
`Drf fields specification <https://www.django-rest-framework.org/api-guide/fields/>`_

.. automodule:: djvue.fields


.. _djvuefields:

DVField
=======

.. autoclass:: DVField
    :members:

DVBooleanField
==============

.. autoclass:: DVBooleanField
    :members:

    .. automethod:: __init__

DVNullBooleanField
==================

.. autoclass:: DVNullBooleanField

    .. automethod:: __init__

DVEmailField
============

.. autoclass:: DVEmailField

DVRegexField
============

.. autoclass:: DVRegexField

DVSlugField
===========

.. autoclass:: DVSlugField

DVURLField
==========

.. autoclass:: DVURLField

DVUUIDField
===========

.. autoclass:: DVUUIDField

DVIPAddressField
================

.. autoclass:: DVIPAddressField

DVIntegerField
==============

.. autoclass:: DVIntegerField

    .. automethod:: __init__

DVFloatField
============

.. autoclass:: DVFloatField

    .. automethod:: __init__

DVDecimalField
==============

.. autoclass:: DVDecimalField

    .. automethod:: __init__

DVDateTimeField
===============

.. autoclass:: DVDateTimeField

    .. automethod:: __init__

DVDateField
===========

.. autoclass:: DVDateField

    .. automethod:: __init__

DVTimeField
===========

.. autoclass:: DVTimeField

    .. automethod:: __init__

DVDurationField
===============

.. autoclass:: DVDurationField

    .. automethod:: __init__

DVMultipleChoiceField
=====================

.. autoclass:: DVMultipleChoiceField

    .. automethod:: __init__

DVFilePathField
===============

.. autoclass:: DVFilePathField

DVFileField
===========

.. autoclass:: DVFileField

DVImageField
============

.. autoclass:: DVImageField

DVListField
===========

.. autoclass:: DVListField

DV_UnvalidatedField
===================

.. autoclass:: DV_UnvalidatedField

DVDictField
===========

.. autoclass:: DVDictField

DVHStoreField
=============

.. autoclass:: DVHStoreField

DVJSONField
===========

.. autoclass:: DVJSONField

DVReadOnlyField
===============

.. autoclass:: DVReadOnlyField

DVHiddenField
=============

.. autoclass:: DVHiddenField

DVSerializerMethodField
=======================

.. autoclass:: DVSerializerMethodField

DVModelField
============

.. autoclass:: DVModelField

DVCharField
===========

.. autoclass:: DVCharField
    :members:

    .. automethod:: __init__

DVChoiceField
=============

.. autoclass:: DVChoiceField
    :members:

    .. automethod:: __init__


DVAutocompletePrimaryKeyRelatedField
====================================

.. automodule:: djvue.relations

.. autoclass:: DVAutocompletePrimaryKeyRelatedField
    :members:

    .. automethod:: __init__


