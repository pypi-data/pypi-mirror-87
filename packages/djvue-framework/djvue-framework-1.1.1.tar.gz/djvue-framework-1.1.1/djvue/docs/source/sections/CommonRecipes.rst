##############
Common recipes
##############


Here you'll find some useful snippets you can take as a reference to get trough some tasks.

|

------------------------------------------------------------------------------------------------------------------------

|

.. _Allow CRUD operations only to some users or disable them at all:

Allow CRUD operations only to some users or disable them at all
===============================================================

It can happens that we want our **DjVue** VieSet to extends those mixins which enable CRUD operations on a model
but perhaps we do not want **DjVue** to show the respective action buttons on the table or maybe we want only some users
to see them.

In order to accomplish this we can override these methods (we'll take as reference the examples
of the :ref:`backend section<Backend>`):

Creation
--------

For the creation operation we will have to override the :code:`allow_creation()` method:

 -  If we want just some users to be able to create model's instances:

    .. code-block:: python

        class ExampleViewSet(DjVueGenericViewSet, ListModelMixin, CreateModelMixin, ...):
            serializer_class = ExampleSerializer
            list_fields = [
                'char_field',
                'int_field',
                'float_field'
            ]

            def allow_creation(self):
                if self.request.user.is_staff:
                    return True
                else:
                    return False

            def get_queryset(self):
                return ModelExample.objects.all()

            ...
       ..

 -  If we want to disable creation operation at all from the **DjVue** table but we still want our ViewSet a working
    endpoint for creation:

    .. code-block:: python

        class ExampleViewSet(DjVueGenericViewSet, ListModelMixin, CreateModelMixin, ...):
            serializer_class = ExampleSerializer
            list_fields = [
                'char_field',
                'int_field',
                'float_field'
            ]

            def allow_creation(self):
                if self.request.user.is_staff:
                    return True
                else:
                    return False

            def get_queryset(self):
                return ModelExample.objects.all()

            ...
        ..

Detail
------

For the detail operation we will have to override the :code:`allow_retrieve()` method:

 -  If we want just some users to be able to get model's instances details:

    .. code-block:: python

        class ExampleViewSet(DjVueGenericViewSet, ListModelMixin, CreateModelMixin, ...):
            serializer_class = ExampleSerializer
            list_fields = [
                'char_field',
                'int_field',
                'float_field'
            ]

            def allow_retrieve(self):
                if self.request.user.is_staff:
                    return True
                else:
                    return False

            def get_queryset(self):
                return ModelExample.objects.all()

            ...
       ..

 -  If we want to disable detail operation at all from the **DjVue** table but we still want our ViewSet a working
    endpoint for retrieval:

    .. code-block:: python

        class ExampleViewSet(DjVueGenericViewSet, ListModelMixin, CreateModelMixin, ...):
            serializer_class = ExampleSerializer
            list_fields = [
                'char_field',
                'int_field',
                'float_field'
            ]

            def allow_retrieve(self):
                if self.request.user.is_staff:
                    return True
                else:
                    return False

            def get_queryset(self):
                return ModelExample.objects.all()

            ...
        ..


Update
------

For the update operation we will have to override the :code:`allow_retrieve()` method:

 -  If we want just some users to be able to update model's instances:

    .. code-block:: python

        class ExampleViewSet(DjVueGenericViewSet, ListModelMixin, CreateModelMixin, ...):
            serializer_class = ExampleSerializer
            list_fields = [
                'char_field',
                'int_field',
                'float_field'
            ]

            def allow_update(self):
                if self.request.user.is_staff:
                    return True
                else:
                    return False

            def get_queryset(self):
                return ModelExample.objects.all()

            ...
       ..

 -  If we want to disable update operation at all from the **DjVue** table but we still want our ViewSet a working
    endpoint for update:

    .. code-block:: python

        class ExampleViewSet(DjVueGenericViewSet, ListModelMixin, CreateModelMixin, ...):
            serializer_class = ExampleSerializer
            list_fields = [
                'char_field',
                'int_field',
                'float_field'
            ]

            def allow_update(self):
                if self.request.user.is_staff:
                    return True
                else:
                    return False

            def get_queryset(self):
                return ModelExample.objects.all()

            ...
        ..


Deletion
--------

For the delete operation we will have to override the :code:`allow_delete()` method:

 -  If we want just some users to be able to delete model's instances:

    .. code-block:: python

        class ExampleViewSet(DjVueGenericViewSet, ListModelMixin, CreateModelMixin, ...):
            serializer_class = ExampleSerializer
            list_fields = [
                'char_field',
                'int_field',
                'float_field'
            ]

            def allow_delete(self):
                if self.request.user.is_staff:
                    return True
                else:
                    return False

            def get_queryset(self):
                return ModelExample.objects.all()

            ...
       ..

 -  If we want to disable delete operation at all from the **DjVue** table but we still want our ViewSet a working
    endpoint for deletion:

    .. code-block:: python

        class ExampleViewSet(DjVueGenericViewSet, ListModelMixin, CreateModelMixin, ...):
            serializer_class = ExampleSerializer
            list_fields = [
                'char_field',
                'int_field',
                'float_field'
            ]

            def allow_delete(self):
                if self.request.user.is_staff:
                    return True
                else:
                    return False

            def get_queryset(self):
                return ModelExample.objects.all()

            ...
        ..

|

------------------------------------------------------------------------------------------------------------------------

|

.. _Add extra redirect buttons on table's rows:

Add extra redirect buttons on table's rows
===========================================

**DjVue** gives us the ability to provide some extra custom redirect buttons on table's rows. For example we could want
a button linked to a custom detail page.

This can be easily achieved overriding the :code:`get_extra_buttons()` method in our ViewSet:

.. code-block:: python

    class ExampleViewSet(DjVueGenericViewSet, ListModelMixin, ...):
        serializer_class = ExampleSerializer
            list_fields = [
                'char_field',
                'int_field',
                'float_field'
            ]

        def get_extra_buttons(self, obj):
            buttons = super(ExampleViewSet, self).get_extra_buttons(obj) # 'buttons' is an array
            buttons.append(RedirectButton(key='detail', props={
                "href": reverse('<url_name>', kwargs={'pk': obj.id}),
                "label": "Details"
            }).__dict__)
            return buttons

        def get_queryset(self):
           return ModelExample.objects.all()

            ...
..

As we did in the :ref:`previous section<Allow CRUD operations only to some users or disable them at all>`, we could want
just some users to see this button:

.. code-block:: python

    class ExampleViewSet(DjVueGenericViewSet, ListModelMixin, ...):
        serializer_class = ExampleSerializer
            list_fields = [
                'char_field',
                'int_field',
                'float_field'
            ]

        def get_extra_buttons(self, obj):
            buttons = super(ExampleViewSet, self).get_extra_buttons(obj) # 'buttons' is an array
            if self.request.user.is_staff:
                buttons.append(RedirectButton(key='detail', props={
                    "baseUrl": reverse('<url_name>', kwargs={'pk': obj.id}),
                    "label": "Details"
                }).__dict__)
            return buttons

        def get_queryset(self):
           return ModelExample.objects.all()

            ...
..

|

------------------------------------------------------------------------------------------------------------------------

|

.. _Hide action buttons (both form and redirect):

Hide action buttons (both form and redirect)
=============================================

Often we just want a plain table with no action so we do not want buttons on the rows' side.
Even if our ViewSet extends just :code:`DjVueGenericViewSet`, :code:`ListModelMixin` (which are required to **DjVue**)
we will have an empty extra column (with no title) on the right side of the table, which only make us waste space on
the table (even if very tight).

In order to remove that useless extra column we can override the :code:`has_extra_buttons()` method in our ViewSet:

.. code-block:: python

    class ExampleViewSet(DjVueGenericViewSet, ListModelMixin, ...):
        serializer_class = ExampleSerializer
            list_fields = [
                'char_field',
                'int_field',
                'float_field'
            ]

        def has_extra_buttons(self)
            return False

        def get_queryset(self):
           return ModelExample.objects.all()

            ...
..

|

------------------------------------------------------------------------------------------------------------------------

|


.. _Avoid using SerializerMethodField:

Avoid using :code:`SerializerMethodField`
=========================================
