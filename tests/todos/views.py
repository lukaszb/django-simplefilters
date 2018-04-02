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
