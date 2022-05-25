# Testing

You should test filtering in the same way you test other parts of the code. This
process is different from project to project. Here we provide some hints how tests
can be implemented for filtering.

## Parametrized tests

Usually when writing tests for filtering we want to assure different behaviours:

- given query param is respected and handled properly
- changing value of that param should yield different results
- wrong values are ignored
- lack of param should yield whole data set

We recommend to use something like pytest's `parametrize` functionality.

```python
@pytest.mark.parametrize('url, expected_todos', [
    ('?status=open', {'todo1'}),
    ('?status=done', {'todo2', 'todo3'}),
    ('?status=done&status=archived', {'todo2', 'todo3', 'todo4'}),
    ('?status=wrong', set()),
    ('?foo=bar', {'todo1', 'todo2', 'todo3', 'todo4'}),
])
def test_list__filter_by_status(arf, url, expected_todos):
    TodoFactory('todo1', status='open')
    TodoFactory('todo2', status='done')
    TodoFactory('todo3', status='done')
    TodoFactory('todo4', status='archived')

    request = arf.get(url)
    response = views.todo_list(request)
    assert response.status_code == 200, response.data
    assert {todo['title'] for todo in response.data} == expected_todos
```

