from .todos import models
from .todos import views
from freezegun import freeze_time
import pytest


pytestmark = pytest.mark.django_db


def test_list(arf):
    todo1 = create_todo('todo1')
    todo2 = create_todo('todo2')
    todo3 = create_todo('todo3')

    request = arf.get('')
    response = views.todo_list(request)
    assert response.status_code == 200, response.data
    assert {todo['id'] for todo in response.data} == {todo1.id, todo2.id, todo3.id}


@pytest.mark.parametrize('url, expected_todos', [
    ('?status=open', {'todo1'}),
    ('?status=done', {'todo2', 'todo3'}),
    ('?status=done&status=archived', {'todo2', 'todo3', 'todo4'}),
    ('?status=wrong', set()),
])
def test_list__filter_by_status(arf, url, expected_todos):
    create_todo('todo1', status='open')
    create_todo('todo2', status='done')
    create_todo('todo3', status='done')
    create_todo('todo4', status='archived')

    request = arf.get(url)
    response = views.todo_list(request)
    assert response.status_code == 200, response.data
    assert {todo['title'] for todo in response.data} == expected_todos


@pytest.mark.parametrize('url, expected_todos', [
    ('?modified_after=2018-04-02T20:00Z', {'todo3', 'todo4'}),
    ('?modified_after=2018-04-02T20:45Z', {'todo3', 'todo4'}),
    ('?modified_after=2018-04-03T00:00Z', {'todo4'}),
    ('?modified_after=2018-05-01T00:00Z', set()),
    ('?modified_after=NOT_A_TIMESTAMP', {'todo1', 'todo2', 'todo3', 'todo4'}),
])
def test_list__filter_by_status(arf, url, expected_todos):
    with freeze_time('2018-04-02T19:15Z'):
        create_todo('todo1')
        create_todo('todo2')
    with freeze_time('2018-04-02T20:45Z'):
        create_todo('todo3')
    with freeze_time('2018-04-03T09:00Z'):
        create_todo('todo4')

    request = arf.get(url)
    response = views.todo_list(request)
    assert response.status_code == 200, response.data
    assert {todo['title'] for todo in response.data} == expected_todos


def create_todo(title='todo', **kwargs):
    return models.Todo.objects.create(title=title, **kwargs)
