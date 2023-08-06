from django.db import models
from django.db.models import BooleanField
from django.db.models import ExpressionWrapper
from django.db.models import Subquery


class BooleanQ(ExpressionWrapper):
    output_field = BooleanField()

    def __init__(self, *args, **kwargs):
        expression = models.Q(*args, **kwargs)
        super().__init__(expression, output_field=None)


class SubquerySum(Subquery):
    template = '(SELECT SUM(%(field_name)s) FROM (%(subquery)s) _sub)'
    output_field = models.IntegerField()

    def __init__(self, queryset, field_name, **kwargs):
        queryset = queryset.order_by()
        if not queryset.query.values_select:
            queryset = queryset.values(field_name)
        super().__init__(queryset, field_name=field_name, **kwargs)


class SubqueryCount(Subquery):
    template = '(SELECT COUNT(*) FROM (%(subquery)s) _sub)'
    output_field = models.IntegerField()

    def __init__(self, queryset, **kwargs):
        queryset = queryset.order_by()
        if not queryset.query.values_select:
            queryset = queryset.values('pk')
        super().__init__(queryset, **kwargs)
