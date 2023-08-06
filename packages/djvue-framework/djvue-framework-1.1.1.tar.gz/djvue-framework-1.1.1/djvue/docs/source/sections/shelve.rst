*******************
Standard operations
*******************

Another **DjVue**'s great feature is the ability to deduce the available operations that can be done on an
:code:`DjVueGenericViewSet` endpoint from the Mixins that it extends.


Creation
========

If our ViewSet extends :code:`CreateModelMixin` then **DjVue** notices it and so it tells the frontend such possibility.

In most cases we'll have to change the serializer in order to pass proper data to the frontend and so render the
related form properly.

When we have a proper serializer for creation we can select the right one in the ViewSet inside
the method :code:`get_serializer_class()` in this way:

.. code-block:: python

   def get_serializer_class(self, *args, **kwargs):
      if self.action in ['create']:
         return ExampleCreateSerializer
      else:
         return ExampleSerializer
..

Perhaps we would like to be able to choose which users can actually create model's instances and which can't.
In this case we can override the :code:`allow_creation()` method this way:

.. code-block:: python

   def allow_creation(self):
      if self.request.user.is_staff:
         return True
      else:
         return False
..

Or we can simply disable creation but still having our ViewSet extending :code:`CreateModelMixin`. We can trivially
do it this way:

.. code-block:: python

   def allow_creation(self):
      return False
..


Update
======

Similar to the creation operation, also for updating if our ViewSet extends :code:`UpdateModelMixin` then **DjVue**
notices it and so it tells the frontend such possibility.

Here as well, we'll likely have to change our serializer in order to pass proper data to the frontend and so render
the related form properly.


When we have a proper serializer for update we can select the right one in the ViewSet inside
the method :code:`get_serializer_class()` in this way:

.. code-block:: python

   def get_serializer_class(self, *args, **kwargs):
      if self.action in ['update', 'partial_update']:
         return ExampleUpdateSerializer
      else:
         return ExampleSerializer
..

As for the creation operation, also for the update we have the possibility to select the users who can actually make
changes to the data

.. code-block:: python

   def allow_update(self):
      if self.request.user.is_staff:
         return True
      else:
         return False
..

Or disabling the updates at all but still having our ViewSet extending :code:`UpdateModelMixin`.

.. code-block:: python

   def allow_update(self):
      return False
..


Deletion
========

Similar to both the creation and update operations, also for deletion if our ViewSet extends :code:`DestoryModelMixin`
then **DjVue** notices it and so it tells the frontend such possibility.

As for both the creation and update operations, also for the deletion we have the possibility to select the users who
can actually delete model's instances overriding the :code:`allow_deletion()` method:

.. code-block:: python

   def allow_deletion(self):
      if self.request.user.is_staff:
         return True
      else:
         return False
..

Or disabling the deletions at all but still having our ViewSet extending :code:`DestoryModelMixin`.

.. code-block:: python

   def allow_update(self):
      return False
..


|

------------------------------------------------------------------------------------------------------------------------

|

*****************
Custom operations
*****************

With **DjVue** we also have the possibility to add some custom redirect operations next to the standard operations of
creation, udate and delete.
This, for example, may be useful in order to link a detail page.

We can achieve this overriding the :code:`get_extra_buttons()` method in our ViewSet:

.. code-block:: python

   def get_extra_buttons(self, obj):
       buttons = super(ExampleViewSet, self).get_extra_buttons(obj) # 'buttons' is an array
       buttons.append(RedirectButton(key='detail', props={
            "baseUrl": reverse('<url_name>', kwargs={'pk': obj.id}),
            "label": "Details"
        }).__dict__)
        return buttons
..

This way a redirect button will be added next to the standard ones.

Very similar to the standard operations we can choose which user can see such button this way:

.. code-block:: python

   def get_extra_buttons(self, obj):
       buttons = super(ExampleViewSet, self).get_extra_buttons(obj) # 'buttons' is an array
       if self.request.user.is_staff:
           buttons.append(RedirectButton(key='detail', props={
               "baseUrl": reverse('<url_name>', kwargs={'pk': obj.id}),
               "label": "Details"
           }).__dict__)
       return buttons
..

|

------------------------------------------------------------------------------------------------------------------------

|


Also suppose to have template view that render a DjVue table listing :code:`ExampleModel`'s objects.
By default, if ViewSet can perform object creation, a button is rendered in the Table component,
and frontend performs a request to get information about the serializer that is bound on create method (POST HTTP method),
once the request has arrived to backend the serializer information are passed back to front, and used in order to
render the form.

In the above example, front receives information about :code:`char_field` and :code:`bool_field` and renders specific
html elements: an :code:`<input type="text">` tag for the first and a :code:`<input type="checkbox">` for the second.
By default, when writing serializers, you can use default DRF's serializers or DjVue overwritten one
but for a full feature behavior we suggest to use DjVue's one,
that because more information are sent to frontend in order to help it to add specific html attributes and
properties like: placeholder, value validation and custom component render.

Inside **DjVue** each field is enclosed into a custom django class, but they are backwards compatible with DRF.