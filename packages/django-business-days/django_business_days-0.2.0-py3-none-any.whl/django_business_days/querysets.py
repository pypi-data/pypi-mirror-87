from datetime import date
from django.db.models import QuerySet, Q


class DayQuerySet(QuerySet):
    def actual_days(self):
        current_year = date.today().year

        return self.filter(
            Q(date__year=current_year, is_repeated=False) | Q(is_repeated=True)
        )
