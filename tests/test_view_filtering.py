from .todos import models
from .todos import views
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


def create_todo(title='todo', **kwargs):
    return models.Todo.objects.create(title=title, **kwargs)
