Changelog
---------

8.5.0 (2020-08-21)
~~~~~~~~~~~~~~~~~~

* Include tri.struct 4.x as possible requirement


8.4.0 (2020-04-24)
~~~~~~~~~~~~~~~~~~

* Fix bulk form missing requests attribute. (Failing on ajax selects)

* Upped dependency tri.declarative to 5.x


8.3.0 (2020-01-09)
~~~~~~~~~~~~~~~~~~

* Change python version to 3.7


8.2.0 (2019-11-21)
~~~~~~~~~~~~~~~~~~

* Introduced `data_retrivial_method`, and turned it on by default for `foreign_key` and `many_to_many`. This means that by default tables are now efficient instead of requiring you to use `prefetch_related` or `select_related` manually.

* Added missing `UUIDField` factory

* Added missing `Column.multi_choice`

* `page_size` wasn't refinable


8.1.1 (2019-10-23)
~~~~~~~~~~~~~~~~~~

* Upped dependency on tri.form due to a bug fix there, and the use of that bug fix in tri.table

* Handle late binding of `request` member of `Table`

* Removed deprecated use of `@creation_ordered`


8.1.0 (2019-10-15)
~~~~~~~~~~~~~~~~~~

* Implemented `Table.actions` as a replacement for `render_table`s argument `links`.

* `Column.multi_choice_queryset` was broken.

* Fixed `many_to_many` shortcut.

* Deprecated the following parameters to `render_table`:
    * `template`: replaced by `Table.template`
    * `paginate_by`: replaced by `Table.page_size`
    * `show_hits`: no replacement
    * `hit_label`: no replacement
    * `page`: no replacement
    * `blank_on_empty`: no replacement
    * `links`: replaced by `Table.actions`

* Bumped dependency tri.declarative to 4.x


8.0.0 (2019-06-14)
~~~~~~~~~~~~~~~~~~

* Renamed module from `tri.table` to `tri_table`

* Dropped support for python2 and Django < 2.0


7.0.2 (2019-05-06)
~~~~~~~~~~~~~~~~~~

* Fixed cases where from_model lost the type when inheriting


7.0.1 (2019-05-03)
~~~~~~~~~~~~~~~~~~

* Fixed a bug where columns that had query or bulk but attr=None would crash


7.0.0 (2019-04-12)
~~~~~~~~~~~~~~~~~~

* Make `Column` shortcuts compatible with subclassing. The previous fix didn't work all the way.

* Use the new major tri.declarative, and update to follow the new style of class member shortcuts

* Removed support for django 1.8

* `bulk_queryset` is now usable to create your own bulk actions without using `Table.bulk_form`

* Bulk form now auto creates via `Form.from_model` correctly

* Query is now auto created via `Query.from_model` correctly

6.3.0 (2019-03-15)
~~~~~~~~~~~~~~~~~~

* Make Column shortcuts compatible with subclassing


6.2.1 (2019-03-05)
~~~~~~~~~~~~~~~~~~

* Fixed a crash when you used a custom paginator in django 2.0+


6.2.0 (2019-03-04)
~~~~~~~~~~~~~~~~~~

* Fixes for jinja2 compatibility (still not fully working)

* `preprocess_data` now takes a new keyword argument `table`

* You can now get the paginator context itself via `Table.paginator_context`

* Paginator template is configurable

* Fixed a bug where we triggered our own deprecation warning for `Column`

* Use the new paginator API for django 2.0+


6.1.0 (2019-01-29)
~~~~~~~~~~~~~~~~~~

* Deprecated `Column` argument `attrs` in favor of `header__attrs`

* Added CSS classes `ascending`/`descending` on headers

* Added ability to customize superheaders via `Column.superheader`

* Added ability to customize `Column` header template via `header__template`

* Deprecated `title` parameter to `Column`

* Deprecated `css_class` parameter to `Column`

* Removed class='row{1,2}' from <tr> tags. This is better accomplished with CSS.


6.0.3 (2018-12-06)
~~~~~~~~~~~~~~~~~~

* Bug fix: "Select all" header button should fire click event, not just toggle the state.


6.0.2 (2018-12-06)
~~~~~~~~~~~~~~~~~~

* Bug fix: "Select all items" question hidden when select all clicked again.

* Bug fix: only show "Select all item" question if a paginator is present.


6.0.1 (2018-12-04)
~~~~~~~~~~~~~~~~~~

* Bug fix: "Select all items" question should only be presented once.


6.0.0 (2018-12-03)
~~~~~~~~~~~~~~~~~~

* Removed argument `pks` to `post_bulk_edit`. This argument is incompatible with non-paginated bulk edit, and it's redundant with the `queryset` argument.

* Added support for bulk editing of an entire queryset, not just the selected items on the current page.

* Fixed bug where the template context was not carried over to the row rendering when using a custom row template.

* Removed `paginator` template tag, moved the functionality into `Table.render_paginator`. This means it can be used from jinja2 and is generally easier to work with.

* Avoid filtering with tri.query if not needed. This means you can now take a slice of a queryset before you pass it to tri.table, if and only if you don't then have filters to apply.

* New feature: refinable attribute `preprocess_data` on `Table`. This is useful if you want to for example display more than one row per result of a queryset or convert the paginated data into a list and do some batch mutation on the items.

* `preprocess_row` returning None is now deprecated. You should now return the row. Just returning the object you were sent is probably what you want.


5.3.1 (2018-10-10)
~~~~~~~~~~~~~~~~~~

* Added `Column.boolean_tristate` for optionally filter boolean fields.

* Add support for setting namespace on tables to be able to reuse column names between two tables in the same view.

* Removed buggy use of `setdefaults`. This could cause overriding of nested arguments to not take.


5.3.0 (2018-08-19)
~~~~~~~~~~~~~~~~~~

* Added `preprocess_row` feature. You can use it to mutate a row in place before access.

* Made `Table` a `RefinableObject`


5.2.2 (2018-06-29)
~~~~~~~~~~~~~~~~~~

* Fix bad mark_safe invocation on custom cell format output.


5.2.1 (2018-06-18)
~~~~~~~~~~~~~~~~~~

* Fixed bug with backwards compatibility for `Link`.


5.2.0 (2018-06-15)
~~~~~~~~~~~~~~~~~~

* New feature: default sort ordering. Just pass `default_sort_order` to `Table`.

* `Link` class is now just inherited from tri_form `Link`. Introduced a deprecation warning for the constructor argument `url`.

* Simplified `prepare` handling for `Table`. You should no longer need to care about this for most operations. You will still need to call `prepare` to trigger the parsing of URL parameters for sorting etc.

* Fixed many_to_many_factory


5.1.1 (2018-04-09)
~~~~~~~~~~~~~~~~~~

* Lazy and memoized BoundCell.value


5.1.0 (2018-01-08)
~~~~~~~~~~~~~~~~~~

* Fix sorting of columns that contains None, this was not working in Python 3


5.0.0 (2017-08-22)
~~~~~~~~~~~~~~~~~~

* Moved to tri.declarative 0.35, tri.form 5.0 and tri.query 4.0. Check release notes for tri.form and tri.query for backwards incompatible changes

* Removed deprecated `template_name` parameter to `render_table`

* Note that `foo__class` to specify a constructor/callable is no longer a valid parameter, because of updated tri.form, use `foo__call_target` or just `foo`


4.3.1 (2017-05-31)
~~~~~~~~~~~~~~~~~~

* Bugfix: sorting on reverse relations didn't work


4.3.0 (2017-04-25)
~~~~~~~~~~~~~~~~~~

* Bugfix for Django 1.10 template handling

* Updated to tri.form 4.7.1

* Moved bulk button inside the table tag

* Dropped support for Django 1.7


4.2.0 (2017-04-21)
~~~~~~~~~~~~~~~~~~

* New feature: post bulk edit callback


4.1.2 (2017-04-19)
~~~~~~~~~~~~~~~~~~

* Fixed silly non-ascii characters in README.rst and also changed to survive silly non-ascii characters in that same file.


4.1.1 (2017-04-10)
~~~~~~~~~~~~~~~~~~

* Fix missing copy of `attrs__class`


4.1.0 (2017-03-22)
~~~~~~~~~~~~~~~~~~

* `Column` class now inherits from `object`, making the implementation more pythonic.
  (Attributes still possible to override in constructor call, see `NamespaceAwareObject`)

* `*.template` overrides can now be specified as `django.template.Template` instances.

* The `template_name` parameter to `render_table` is now deprecated and superceeded by a `template` parameter.


4.0.0 (2016-09-15)
~~~~~~~~~~~~~~~~~~

* Updated to newest tri.form, tri.query, tri.declarative. This gives us simpler factories for `from_model` methods.

* Added shortcuts to `Column`: `time` and `decimal`

* The following shortcuts have been updated to use the corresponding `Variable` shortcuts: date, datetime and email

* Fix failure in endpoint result return on empty payload.
  `[]` is a valid endpoint dispatch result.

* `render_table`/`render_table_to_response` no longer allow table to be passed as a positional argument


3.0.1 (2016-09-06)
~~~~~~~~~~~~~~~~~~

* Fix crash on unidentified sort parameter.


3.0.0 (2016-09-02)
~~~~~~~~~~~~~~~~~~

* `bound_row` is passed to row level callables. This is a potential breaking
  change if you didn't do `**_` at the end of your function signatures (which you
  should!)

* `bound_row` and `bound_column` is passed to cell level callables. This is a
  potential breaking change like above.

* `BoundRow` now supports `extra`.

* compatibible with Django 1.9 & 1.10

* Added strict check on the kwargs config namespace of `Table`

* Added `extra` namespace to `Table`

* Added `bound_cell` parameter to rendering of cell templates.


2.5.0 (2016-07-14)
~~~~~~~~~~~~~~~~~~

* Added optional `endpoint_dispatch_prefix` table configuration to enable multiple
  tables on the same endpoint.


2.4.0 (2016-07-13)
~~~~~~~~~~~~~~~~~~

* Made more parts of `BoundCell` available for reuse.


2.3.0 (2016-07-12)
~~~~~~~~~~~~~~~~~~

* Added pass-through of extra arguments to `Link` objects for custom attributes.


2.2.0 (2016-06-23)
~~~~~~~~~~~~~~~~~~

* Fix missing namespace collection for column custimization of Table.from_model


2.1.0 (2016-06-16)
~~~~~~~~~~~~~~~~~~

* Renamed `db_compat.register_field_factory` to the clearer `register_column_factory`

* Improved error reporting on missing django field type column factory declaration.

* Added iteration interface to table to loop over bound rows

* Added `endpoint` meta class parameter to table to enable custom json endpoints


2.0.0 (2016-06-02)
~~~~~~~~~~~~~~~~~~

* Support for ajax backend

* Dependent tri.form and tri.query libraries have new major versions


1.16.0 (2016-04-25)
~~~~~~~~~~~~~~~~~~~

* Minor bugfix for fields-from-model handling of auto fields


1.15.0 (2016-04-21)
~~~~~~~~~~~~~~~~~~~

* Table.from_model implemented


1.14.0 (2016-04-19)
~~~~~~~~~~~~~~~~~~~

* Added `after` attribute on `Column` to enable custom column ordering (See `tri.declarative.sort_after()`)

* Enable mixing column definitions in both declared fields and class meta.

* Don't show any results if the form is invalid


1.13.0 (2016-04-08)
~~~~~~~~~~~~~~~~~~~

* Add python 3 support


1.12.0 (2016-02-29)
~~~~~~~~~~~~~~~~~~~

* Changed syntax for specifying html attributes and classes. They are now use the same way of addressing as
  other things, e.g.: Column(attrs__foo="bar", attrs__class__baz=True) will yield something like
  `<th class="baz" foo=bar>...</th>`


1.11.0 (2016-02-04)
~~~~~~~~~~~~~~~~~~~

* Fix missing evaluation of row__attr et al.


1.10.0 (2016-01-28)
~~~~~~~~~~~~~~~~~~~

* Changed cell__template and row__template semantics slightly to enable customized cell ordering in templates.

  row__template implementations can now access a BoundCell object to use the default cell rendering.

  cell__template implementation are now assumed to render the <td> tags themself.


1.9.0 (2016-01-19)
~~~~~~~~~~~~~~~~~~

* Fixed to work with latest version of tri.form
