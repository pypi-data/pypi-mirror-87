########
Frontend
########

Setup
=====

The frontend part is way more simple, as almost all the work is done by the **DjVue** frontend system on top of the Vue
framework.
All we have to do here is to include all the css/javascript dependencies:

.. TODO

.. code-block:: python

    # TODO
..

Or if our using Django as frontend as well, we can use **DjVue** templatetags and put those inside the :code:`<head>`
tag in the following way:

.. code-block:: html

   {% load djvue %}

   <head>
      ...
      {% djvue_css %}
      {% vue_javascript %}
      {% djvue_javascript %}
      ...
   </head>
..

Included the dependencies we can already create a **DjVue** instance inside our javascript in order to select an empty
:code:`<div>` within our html trough an id and fill it with the table in the following way:

.. code-block:: html

   <body>
      ...
      <div id="table-id"></div>
      ...
   </body>

   ...

   <script>
      ...
      $(document).ready(function () {
            var table = new djvue.Table({
                el: '#table-id', // <-- jQuery selector
                propsData: {
                    baseUrl: "<viewset_url>",// Or "{% url 'example-list' %}" (in our example) if we are using Django
                    tableProps :{
                        // Here we enter the properties of the table
                    },
                },
            });

        });
      ...
   </script>
..

|

------------------------------------------------------------------------------------------------------------------------

|

Table properties
================

Down here all properties you can use to customize the table appearance.
They are nothing more than a selection of Boostrap-vue table's properties.
If you want a further description about them you can refer to `this`_ page.

.. list-table::
   :header-rows: 1

   * - Property
     - Type
     - Default
     - Description
   * - :code:`striped`
     - :code:`Boolean`
     - :code:`false`
     - Applies striping to the tbody rows
   * - :code:`borderless`
     - :code:`Boolean`
     - :code:`false`
     - Removes all borders from cells
   * - :code:`outlined`
     - :code:`Boolean`
     - :code:`false`
     - Adds an outline border to the table element
   * - :code:`dark`
     - :code:`Boolean`
     - :code:`false`
     - Places the table in dark mode
   * - :code:`hover`
     - :code:`Boolean`
     - :code:`false`
     - Enables hover styling on rows
   * - :code:`small`
     - :code:`Boolean`
     - :code:`false`
     - Renders the table with smaller cell padding
   * - :code:`fixed`
     - :code:`Boolean`
     - :code:`false`
     - Makes all columns equal width (fixed layout table).
       Will speed up rendering for large tables.
       Column widths can be set via CSS or colgroup.
   * - :code:`responsive`
     - :code:`Boolean` or :code:`String`
     - :code:`false`
     - Makes the table responsive in width, adding a horizontal scrollbar.
       Set to true for always responsive or set to one of the breakpoints
       to switch from responsive to normal: 'sm', 'md', 'lg', 'xl'.
   * - :code:`sticky-header`
     - :code:`Boolean` or :code:`String`
     - :code:`false`
     - Makes the table header sticky. Set to true for a maximum
       height 300px tall table, or set to any valid CSS hight (including units).
   * - :code:`no-border-collapse`
     - :code:`Boolean`
     - :code:`false`
     - Disable's the collapsing of table borders. Useful when table has sticky headers or columns
   * - :code:`table-variant`
     - :code:`String`
     -
     - Apply a Bootstrap theme color variant to the entire table
   * - :code:`table-class`
     - :code:`String` or :code:`Array` or :code:`Object`
     -
     - CSS class (or classes) to apply to the table element
   * - :code:`stacked`
     - :code:`Boolean` or :code:`String`
     - :code:`false`
     - Place the table in stacked mode. Set to true for always stacked,
       or set to one of the breakpoints to switch from stacked to normal: 'sm', 'md', 'lg', 'xl'
   * - :code:`head-variant`
     - :code:`String`
     -
     - Header variant: 'light' or 'dark', or unset. May take precedence over head-row-variant
   * - :code:`head-row-variant`
     - :code:`String`
     -
     - Apply a Bootstrap theme color variant to the tr element in the thead
   * - :code:`thead-class`
     - :code:`String` or :code:`Array` or :code:`Object`
     -
     - CSS class (or classes) to apply to the thead element
   * - :code:`thead-tr-class`
     - :code:`String` or :code:`Array` or :code:`Object`
     -
     - CSS class (or classes) to apply to the tr element in the thead
   * - :code:`foot-clone`
     - :code:`Boolean`
     - :code:`false`
     - Enable to the footer of the table, and clone the header content by default
   * - :code:`foot-variant`
     - :code:`String`
     -
     - Footer variant: 'light' or 'dark', or unset. May take precedence over foot-row-variant
   * - :code:`foot-row-variant`
     - :code:`String`
     -
     - Apply a Bootstrap theme color variant to the tr element in the tfoot. Falls back to head-row-variant
   * - :code:`tfoot-class`
     - :code:`String` or :code:`Array` or :code:`Object`
     -
     - CSS class (or classes) to apply to the tfoot element
   * - :code:`tfoot-tr-class`
     - :code:`String` or :code:`Array` or :code:`Object`
     -
     - CSS class (or classes) to apply to the tr element in the tfoot
   * - :code:`tbody-tr-class`
     - :code:`String` or :code:`Array` or :code:`Object` or :code:`Function`
     -
     - CSS class (or classes) to apply to the tr element in the tbody. Can be a function that returns a class
   * - :code:`tbody-tr-attr`
     - :code:`Object` or :code:`Function`
     -
     - Attributes to be added to each tr in the tbody, or a function returning such attributes (see docs for details)
   * - :code:`details-td-class`
     - :code:`String` or :code:`Array` or :code:`Object`
     -
     - CSS class (or classes) to apply to the row details' `td` element for the row-details slot
   * - :code:`tbody-transition-props`
     - :code:`Object`
     -
     - Vue 'transition-group' properties. When provided will make the tbody a Vue 'transition-group' component
   * - :code:`tbody-class`
     - :code:`String` or :code:`Array` or :code:`Object`
     -
     - CSS class (or classes) to apply to the tbody element
   * - :code:`caption`
     - :code:`String`
     -
     - Text string to place in the caption element
   * - :code:`caption-html`
     - :code:`String`
     -
     - HTML string to place in the caption element. Use with caution
   * - :code:`show-empty`
     - :code:`Boolean`
     - :code:`false`
     - When enabled, and there are no item records to show, shows a message that there are no rows to show
   * - :code:`empty-text`
     - :code:`String`
     - :code:`'There are no records to show'`
     - Text string to show when the table has no items to show
   * - :code:`empty-html`
     - :code:`String`
     -
     - HTML string to show when the table has no items to show. Use with caution
   * - :code:`empty-filtered-text`
     - :code:`String`
     - :code:`'There are no records matching your request'`
     - Text string to show when the table has no items to show due to filtering
   * - :code:`empty-filtered-html`
     - :code:`String`
     -
     - HTML string to show when the table has no items to show due to filtering. Use with caution
..


.. _this: https://bootstrap-vue.org/docs/components/table#comp-ref-b-table-props

|

------------------------------------------------------------------------------------------------------------------------

|

Forms Component
===============

One of the most interesting part of **DjVue** is the ability to render frontend form dynamically based on serializer fields, avoid writing custom forms. Once frontend has retrieved information about serializer field it render a html form. **DjVue** has a builtin system that render specific html element based on :code:`type` field value and other fields, but this behavior can be overwriten by specifying :code:`widget` parameter into DjVue serializer field (when available).

Table below shows available html widgets that can be rendered by frontend

.. list-table::
    :header-rows: 1

    * - Widget
      - Description
      - Note
    * - :code:`input`
      - Generic html input
      - Based on :code:`type` value many other input type can be rendered like checkboxes radio button and date field
    * - :code:`select`
      - A dropdown select to choose from a set of values
      - Autocomplete and search can be added
    * - :code:`textarea`
      - A resizable textarea usefull for long texts
      -
..

Table below shows the default widget rendered by front relatively to serializer field and other parameter

.. list-table::
    :header-rows: 1

    * - Serializer Field
      - Html tag
      - Note
    * - :code:`DVBooleanField`
      - :code:`<input type='checkbox'>`
      - Checkbox
    * - :code:`DVNullBooleanField`
      - :code:`<input type='checkbox'>`
      - Checkbox
    * - :code:`DVEmailField`
      - :code:`<input type='email'>`
      -
    * - :code:`DVIntegerField`
      - :code:`<input type='number'>`
      - If limits are specified in serializer, like :code:`max_value` and :code:`max_value` value is limited
    * - :code:`DVFloatField`
      - :code:`<input type='number'>`
      - If limits are specified in serializer, like :code:`max_value` and :code:`max_value` value is limited
    * - :code:`DVDecimalField`
      - :code:`<input type='number'>`
      - If limits are specified in serializer, like :code:`max_value` and :code:`max_value` value is limited
    * - :code:`DVDateTimeField`
      - :code:`<input type='datetime-local'>`
      -
    * - :code:`DVDateField`
      - :code:`<input type='date'>`
      -
    * - :code:`DVTimeField`
      - :code:`<input type='time'>`
      -
    * - :code:`DVMultipleChoiceField`
      - :code:`<input type='checkbox'>`
      - A checkbox list of available options
    * - :code:`DVCharField`
      - :code:`<input type='text'>`
      -
    * - :code:`DVChoiceField`
      - :code:`<input type='radio'>`
      - A radio button list of available options
    * - :code:`DVAutocompletePrimaryKeyRelatedField`
      -
      - A VueJs component with search, pagination and multiselect features

..
