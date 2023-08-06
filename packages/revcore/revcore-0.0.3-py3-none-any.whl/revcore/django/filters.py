from django.conf import settings
from pytz import timezone
import datetime
from rest_framework import filters, exceptions

TIME_ZONE = settings.TIME_ZONE


class DateFilterBackend(filters.BaseFilterBackend):
    def get_time_range(self, from_date, to_date):
        try:
            year, month, day = from_date.split('-')
            tzinfo = timezone(TIME_ZONE)
            from_date = datetime.datetime(int(year), int(month), int(day), tzinfo=tzinfo)

            year, month, day = to_date.split('-')
            to_date = datetime.datetime(int(year), int(month), int(day))
            to_date = to_date.combine(to_date, datetime.time.max, tzinfo=tzinfo)

            return [from_date, to_date]
        except:
            raise exceptions.ValidationError

    def get_context(self, view, time_range):
        date_fields = getattr(view, 'date_fields', [])
        context = {}

        for field in date_fields:
            context["{}__range".format(field)] = time_range

        return context

    def filter_queryset(self, request, queryset, view):
        from_date = request.query_params.get('from', None)
        to_date = request.query_params.get('to', None)

        if not from_date or not to_date:
            return queryset

        time_range = self.get_time_range(from_date, to_date)
        context = self.get_context(view, time_range)
        return queryset.filter(**context)
