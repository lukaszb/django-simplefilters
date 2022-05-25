---
sidebarDepth: 2
---

# Quickstart

This is a drop-in replacement for built-in Django Rest Framework filters
package. It provides an easy way to retrieve params from the URL and use them to
narrow results of the queryset.

## Installation

```shell
$ pip install django-simplefilters
```

## Basic Usage

First, let's define our filterset.

```python
import simplefilters as filters


class Todo(filters.FilterSet):

    @filters.CharFilter(many=True)
    def filter_status(self, qs, values):
        return qs.filter(status__in=values)

    @filters.DateTimeFilter()
    def filter_min_modify_date(self, qs, value):
        return qs.filter(modified_at__gte=value)
```


Now let's connect our filterset with some viewset.


```python
from . import filtersets
from . import models
from . import serializers
from rest_framework.viewsets import ModelViewSet
import simplefilters as filters


class TodoViewSet(ModelViewSet):
    queryset = models.Todo.objects.all()
    serializer_class = serializers.Todo
    filter_backends = [filters.DjangoFilterBackend]
    filter_class = filtersets.Todo

    class Meta:
        model = models.Todo


todo_list = TodoViewSet.as_view({'get': 'list'})
```

::: tip
You can also use filtersets with
- [api views](/guide/drf.html#view)
- [plain Django views](/guide/django#django-view)
- or even [outside of request-response cycle](/guide/django#call-filterset-directly)
:::

Read more about [built-in filters](/api/filters.html#basefilter).

## What is django-simplefilters

The main difference with other solutions, i.e.
[django-filter](https://pypi.python.org/pypi/django-filter), is that we do not
try to handle each case and actual filtering is left for the user to implement.
This might sound counterintuitive for a filtering library but we believe that in
many cases it's much easier to write something like

```python
class EntryFilterSet(filters.FilterSet):

    @filters.CharFilter(many=True)
    def filter_status(self, queryset, values):
        return queryset.filter(status__in=values)
```

than try to find this special case (multiple values) in your filtering library documentation.


## Motivation

We've been using `django-filter` for a long time and it's really great library. However,
due to how many possibilites it offer, we've found out that sometimes it's really hard to find
proper portion of the documentation. Sometimes we really hoped that we could simply define
a method and write queryset filtering by hand (hint: [it is possible](https://django-filter.readthedocs.io/en/main/ref/filters.html#method)).

The other side of the story is **maintability**. Even if someone already spend some time fiddling
with the filterset and reading documentation - it was still sometimes difficult to get back to this
code after some time. Here is an example from [django-filter docs]():

```python
class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'name': ['exact'],
            'release_date': ['isnull'],
        }
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }
```

After reading this code would you be able to tell what filters are supported and
how exactly filtering would be applied to the queryset? :thinking:

`django-simplefilters` is less flexible, more opinionated and definitely more explicit.
