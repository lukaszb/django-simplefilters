# Plain Django

While `django-simplefilters` were built with Django Rest Framework in mind
it's really easy to use it with plain Django views too.


## Filterset

Let's define our filtering as usual.

```python
import simplefilters as filters


class Todo(filters.FilterSet):

    @filters.CharFilter(many=True)
    def filter_status(self, qs, values):
        return qs.filter(status__in=values)

    @filters.DateTimeFilter()
    def filter_modified_after(self, qs, value):
        return qs.filter(modified_at__gte=value)
```

## Django view

```python
from . import filtersets
from . import models
from django.http import JsonResponse
import simplefilters as filters


def todo_list_view(request):
    queryset = models.Todo.objects.all()
    fs = filtersets.Todo()
    qs = fs.perform_filtering_for_query_params(queryset, request.GET)
    return JsonResponse([{
        "id": todo.id,
        "title": todo.title,
    } for todo in qs], safe=False)
```


## Call filterset directly

It is possible to use `simplefilters` out of request-response cycle.

```python
from . import filtersets
from . import models
from . import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import simplefilters as filters


def get_todos(params):
    queryset = models.Todo.objects.all()
    fs = filtersets.Todo()
    return fs.perform_filtering_for_query_params(queryset, {'status': ['active', 'archived']})
```
