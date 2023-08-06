from datetime import datetime, date
from typing import List

from business.calendar import Calendar

from .models import Day

__all__ = (
    'get_calendar'
)

def get_calendar() -> Calendar:
    holidays = prepare_dates(get_holidays())
    extra_working_days = prepare_dates(get_extra_working_days())

    return Calendar(holidays=holidays, extra_working_dates=extra_working_days)


def get_holidays():
    return (
        Day
        .objects
        .filter(is_holiday=True)
        .actual_days()
        .values_list('date', flat=True)
    )


def get_extra_working_days():
    return (
        Day
        .objects
        .filter(is_holiday=False)
        .actual_days()
        .values_list('date', flat=True)
    )


def prepare_dates(days):
    current_year = datetime.today().year

    return set([day.replace(year=current_year) for day in days])
