'''
Should be used as drop-in replacement of drf filters.

Example::

    class EntryListFilterSet(filters.FilterSet):

        @filters.CharFilter(many=True)
        def filter_status(self, qs, values):
            return qs.filter(status__in=values)

        class Meta:
            model = models.Entry

'''
from rest_framework.filters import *  # NOQA
import dateutil.parser
import logging


log = logging.getLogger(__file__)


class DjangoFilterBackend:

    def filter_queryset(self, request, queryset, view):
        filter_class = getattr(view, 'filter_class')
        if not filter_class:
            return queryset
        filter_obj = filter_class()
        return filter_obj.perform_filtering(request, queryset, view)


class FilterSet:

    def perform_filtering(self, request, queryset, view):
        self.request = request
        self.queryset = queryset
        self.view = view

        queryset = self.perform_filtering_for_query_params(queryset, request.query_params)
        return queryset

    def perform_filtering_for_query_params(self, queryset, query_params):
        for filter, value in self.iter_filters_and_values(query_params):
            queryset = filter.method(self, queryset, value)
        return queryset

    def iter_filters_and_values(self, query_params):
        all_filters = self.get_filter_methods()
        for filter in all_filters:
            value = filter.get_value(query_params)

            if value is not None:
                yield filter, value

    def get_filter_methods(self):
        attrs_names = dir(self)
        attrs = [getattr(self, name) for name in attrs_names]

        def marked_as_filter_method(attr):
            return isinstance(attr, BaseFilter)

        filter_methods = [attr for attr in attrs if marked_as_filter_method(attr)]
        return filter_methods


class BaseFilter:

    def __init__(self, param=None, many=False):
        self.param = param
        self.many = many

    def __call__(self, method):
        self.method = method
        if not self.param:
            self.param = self.get_param_name_for_method(method)
        return self

    def get_param_name_for_method(self, method):
        if not method.__name__.startswith('filter_'):
            raise Exception("Filter method must be prefixed with 'filter_'")
        return method.__name__.split('filter_', 1)[1]

    def get_value(self, params):
        if self.param in params:
            if self.many:
                values = params.getlist(self.param)
                values = [self.get_single_value(v) for v in values]
                values = [v for v in values if v is not None]
                if values:
                    return values
                else:
                    return None
            else:
                value = params[self.param]
                return self.get_single_value(value)
        else:
            return None

    def get_single_value(self, value):
        return value


class CharFilter(BaseFilter):
    pass


class IntegerFilter(BaseFilter):

    def get_single_value(self, value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return None


class FlagFilter(BaseFilter):

    def get_single_value(self, value):
        if value.lower() in ['y', 'yes', 't', 'true', '1']:
            return True
        elif value.lower() in ['n', 'no', 'f', 'false', '0']:
            return False
        else:
            log.warn("Unrecognized param for flag filter: %r" % value)


class DateTimeFilter(BaseFilter):

    def get_single_value(self, value):
        try:
            return dateutil.parser.parse(value)
        except ValueError:
            # Wrong timestamps should be ignored
            log.debug("Wrong timestamp filter value: %r" % value)
            return None
