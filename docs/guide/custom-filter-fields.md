
# Custom filters

It's pretty easy to write your own filter. `BaseFilter` yields raw string value
directly from query string. You'd need to subclass that filter and overwrite
`get_single_value(self, value)` method.


## Example

Let's say we want to write a filter that would only recognize `yes` or `no` values
and convert them into `True` or `False`. However, if user provides wrong value
we would return `HTTP 400` response.

```python
from rest_framework.exceptions import ValidationError
import simplefilters as filters


class FlagFilter(filters.BaseFilter):

    def get_single_value(self, value):
        if value == 'yes'
            return True
        elif value == 'no':
            return False
        else:
            msg = f'unrecognized querystring value: {value!r}'
            raise ValidationError({'detail': msg})
```

