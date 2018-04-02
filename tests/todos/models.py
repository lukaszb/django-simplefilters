from django.db import models


StatusChoices = (
    ('open', 'open'),
    ('done', 'done'),
    ('archived', 'archived'),
)


class Todo(models.Model):
    title = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=16, choices=StatusChoices, default='open')
    tags = models.ManyToManyField('Tag')

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.name
