from django.utils import timezone
import simplefilters as filters


def test_value_is_converted_to_datetime_object():
    param_value = '2018-04-02T20:00Z'
    expected_value = aware_datetime(2018, 4, 2, 20)
    filter = filters.DateTimeFilter()
    assert filter.get_single_value(param_value) == expected_value


def aware_datetime(*args):
    return timezone.make_aware(timezone.datetime(*args))
