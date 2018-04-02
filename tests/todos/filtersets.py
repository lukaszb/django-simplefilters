import simplefilters as filters


class Todo(filters.FilterSet):

    @filters.CharFilter(many=True)
    def filter_status(self, qs, values):
        return qs.filter(status__in=values)
