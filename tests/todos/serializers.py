from . import models
from rest_framework import serializers


class Todo(serializers.ModelSerializer):

    class Meta:
        model = models.Todo
        fields = (
            'id',
            'title',
            'created_at',
            'modified_at',
            'status',
        )
