---
sidebarDepth: 3
---

# FilterSet



## perform_filtering

```python
def perform_filtering(request, queryset, view=None)
```

Main entry point of the filterset. This method is called by DRF filter backends
executor.

**Params**

- `request`: instance of `rest_framework.request.Request`
- `queryset`: Django's queryset object
- `view`: (optional) view/viewset object. It's actually not used by `django-simplefilters` but is part of the protocol and is passed by DRF.

## perform_filtering_for_query_params

```python
def perform_filtering_for_query_params(queryset, query_params)
```

Actual filtering.

**Params**

- `queryset`: Django's queryset object
- `query_params`: `QueryDict` / `dict` with url query params


## iter_filters_and_values

```python
def iter_filters_and_values(query_params)
```

Generator that yields tuples of `(filter, value)` matched with given `query_params`.

**Params**

- `query_params`: `QueryDict` / `dict` with url query params



## get_filter_methods

```python
def get_filter_methods()
```

Returns all filter methods defined at the filterset.
