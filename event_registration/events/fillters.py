from django.utils.timezone import make_aware
from datetime import datetime


def filter_by_type(queryset, event_type):
    """
    Filters events by their type.
    """
    return queryset.filter(event_type=event_type) if event_type else queryset


def filter_by_specific_date(queryset, event_date):
    """
    Filters events by a specific date.
    """
    if event_date:
        aware_date = make_aware(datetime.strptime(event_date, '%Y-%m-%d'))
        return queryset.filter(date_time__date=aware_date)
    return queryset


def filter_by_date_range(queryset, start_date, end_date):
    """
    Filters events within a range of start_date and end_date.
    """
    if start_date:
        aware_start_date = make_aware(datetime.strptime(start_date, '%Y-%m-%d'))
        queryset = queryset.filter(date_time__gte=aware_start_date)
    if end_date:
        aware_end_date = make_aware(datetime.strptime(end_date, '%Y-%m-%d'))
        queryset = queryset.filter(date_time__lte=aware_end_date)
    return queryset
