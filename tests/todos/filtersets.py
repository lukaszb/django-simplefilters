import simplefilters as filters


class Todo(filters.FilterSet):

    @filters.CharFilter(many=True)
    def filter_status(self, qs, values):
        return qs.filter(status__in=values)

    @filters.DateTimeFilter()
    def filter_modified_after(self, qs, value):
        return qs.filter(modified_at__gte=value)
