# DRF

## Filterset


Now let's take a look at the `filtersets.py` - here we define filtering
of our viewset.


```python
# filtersets.py
import simplefilters as filters


class Todo(filters.FilterSet):

    @filters.CharFilter(many=True)
    def filter_status(self, qs, values):
        return qs.filter(status__in=values)

    @filters.DateTimeFilter()
    def filter_modified_after(self, qs, value):
        return qs.filter(modified_at__gte=value)

```


## Viewset

Here is a pretty standard viewset for `Todo` model. Note that
at this point we simply replace DRF's `filters` with `simplefilters`.

```python{6}
# views.py
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

## View

It's easy to use filtersets at plain DRF api views too.


```python
from . import filtersets
from . import models
from . import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
import simplefilters as filters

@api_view(['GET'])
def todo_list(request):
    queryset = models.Todo.objects.all()
    fs = filtersets.Todo()
    qs = fs.perform_filtering(request, queryset)
    serializer = serializers.Todo(qs, many=True)
    return Response(serializer.data)
```


