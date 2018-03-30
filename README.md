# django-simplefilters

This is a drop-in replacement for built-in Django Rest Framework filters package. It provides an easy way to retrieve params from the URL and use them to narrow results of the queryset.

The main difference with other solutions, i.e. [django-filter](https://pypi.python.org/pypi/django-filter), is that we do not try to handle each case and actual filtering is left for the user to implement. This might sound counterintuitive for a filtering library but we believe that in many cases it's much easier to write something like

    class EntryFilterSet(filters.FilterSet):

        @filters.CharFilter(many=True)
        def filter_status(self, queryset, values):
            return queryset.filter(status__in=values)

than try to lookup this special case (multiple values) in your filtering library documentation.



## Installation

    $ pip install django-simplefilters


## Usage

Let's imagine we have an `Entry` model with following attributes:

    status_choices = ((c, c) for c in ['draft', 'published', 'archived'])

    class Entry(models.Model):
        title = models.CharField(max_length=64)
        status = models.CharField(max_length=16, choices=status_choices)
        modified_at = models.DateTimeField(auto_now=True)


and we want to allow owner to filter entries by their status and modification date.

We need to define our filterset first:


    # entries/filtersets.py
    import simplefilters as filters


    class Entry(filters.FilterSet):

        @filters.CharFilter()
        def filter_status(self, queryset, value):
            return queryset.filter(status=value)

        @filters.DateTimeFilter()
        def filter_modified_at_min(self, queryset, ts):
            return queryset.filter(modified_at__gte=ts)

        @filters.DateTimeFilter()
        def filter_modified_at_max(self, queryset, ts):
            return queryset.filter(modified_at__lte=ts)


Mostly this should be self-explanatory, however important bit is how we indicate url param. This is achieved similarly to validation in serializers: name of the parameter is prefixed with `filter_` string. So, code above defines filters for following URL parameters: `status`, `modified_at_min` and `modified_at_max`.

Then hook it at corresponding ViewSet class:

    # entries/views.py
    from . import filtersets
    from . import models
    import simplefilters as filters


    class EntryViewSet(ModelViewSet):
        serializer_class = ...
        filter_backends = [filters.DjangoFilterBackend]
        filter_class = filtersets.Entry

        class Meta:
            model = models.Entry


now user would be able to perform queries like:

    GET /entries?status=draft
    GET /entries?modified_at_min=2018-03-30T14:00Z
    etc.




## Supported filters

By definition, whatever user puts as query param is simply a string. Thus, `CharFiled` is simplest and most basic filter. But sometimes we would need to accept other types, i.e. numbers, timestamps or flags.

Here is a full list of available filters:

### `CharFilter`

Most basic filter. Nothing fancy is done here.

### `IntegerFilter`

Param is casted to integer.

### `FlagFilter`

Param is casted to bool. Strings that would be treated as `True` indicator (case insensitive): `yes`, `y`, `true`, `t` and `1`. Similarly, those would be treated as `False`: `no`, `n`, `false`, `f` and `0`.

### `DateTimeFilter`

Param is casted to `datetime` object.


## Multiple params

Sometimes we want to pass multiple params from the url. In example, we might want to allow users to filter by multiple status values and perform something like:

    GET /entries?status=draft&status=archived


For this to work, simply indicate that we want to use `many` values at the filter method definition:

      @filters.CharFilter(many)
      def filter_status(self, queryset, values):
          return queryset.filter(status__in=values)
