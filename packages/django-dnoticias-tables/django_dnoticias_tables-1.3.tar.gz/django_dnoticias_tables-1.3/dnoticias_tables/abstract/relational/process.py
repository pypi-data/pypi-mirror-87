import logging
import math
from ..abstract_process import AbstractProcess
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import formats, timezone
try:
    from polymorphic.models import PolymorphicModel
except ImportError as identifier:
    PolymorphicModel = type(None)
from datetime import datetime

logger = logging.getLogger(__name__)


class Process(AbstractProcess):
    def produce_query_set(self):
        qs = Q()
        if len(self.global_search):
            queries = [
                Q(**{f: self.global_search}) for f in self.searchable_fields
            ]
            for query in queries:
                qs = qs | query
        self.queryset = self.queryset.filter(qs).order_by(self.order_direction + self.orderable_fields[self.order_column]).distinct()
        return self.queryset

    def post_config(self):
        self.paginator = Paginator(self.queryset, self.length)  # items per page
        page_number = math.ceil((self.start + self.length) / self.length)
        page_number = page_number if page_number <= self.paginator.num_pages else 1
        page = self.paginator.page(page_number)
        return page.object_list

    def resolve_best_value(self, instance, field):
        try:
            return getattr(instance, "get_{}_display".format(field))()
        except:
            value = getattr(instance, field, None)
            return self._get_best_value(value)

    def _get_best_value(self, value):
        if isinstance(value, datetime):
            return formats.date_format(
                timezone.localtime(value),
                'SHORT_DATETIME_FORMAT'
            )
        elif isinstance(value, bool):
            return value
        elif value is None:
            return None
        elif issubclass(type(value), PolymorphicModel):
            return str(type(value)._default_manager.get(pk=value.pk))
        else:
            temp = str(value)
            return temp

    def get_instance_id(self, item):
        return item.pk
