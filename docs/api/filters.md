---
sidebarDepth: 3
---


# Built-in Filters

## BaseFilter

```python
def __init__(param=None, many=False)
```

**Params**

- `param`: (optional) Name of the query param. If not explicitly provided would be taken
  from the function name. I.e. for `def filter_modified_at_min` name of the query param
  would be `modified_at_min`, for `def filter_status` it would be `status`.

  Example:

  ```python
  # would match '?s=new' and not '?status=new'
  @filters.CharField("s")
  def filter_status(self, qs, value):
      return qs.filter(status__in=values)
  ```

- `many`: If set to `True` array of values would be passed to filter function instead of
  a single value. Multiple values for single param is supported, i.e. `?status=new&status=in_progress`.
  Then `values` would be `['new', 'in_progress']`:

  ```python
  # query string: '?status=new&status=in_progress'
  @filters.CharField(many=True)
  def filter_status(self, qs, values):
      # values: ['new', 'in_progress']
      return qs.filter(status__in=values)
  ```

## CharField

**Example**

```python
@filters.CharFilter()
def filter_status(self, qs, value):
    return qs.filter(status=value)
```


## IntegerFilter

**Example**

```python
@filters.CharFilter()
def filter_status(self, qs, value):
    return qs.filter(status=value)
```

## FlagFilter

- Truthy values: `['y', 'yes', 't', 'true', '1']` (case insensitive)
- Falsy values: `['n', 'no', 'f', 'false', '0']` (case insensitive)

**Example**

```python
@filters.FlagFilter()
def filter_is_active(self, qs, value):
    # value would be True for: '?is_active=y', '?is_active=yes', '?is_active=t' etc
    # value would be False for: '?is_active=n', '?is_active=no', '?is_active=f' etc
    return qs.filter(is_active=value)
```

## DateTimeFilter

```python
@filters.DateTimeFilter()
def filter_modified_after(self, qs, value):
    return qs.filter(modified_at__gte=value)
```
