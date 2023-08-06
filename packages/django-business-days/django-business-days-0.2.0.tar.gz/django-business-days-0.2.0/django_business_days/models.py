from django.db import models
from django.utils.translation import pgettext_lazy

from .querysets import DayQuerySet


__all__ = (
    'Day',
)


class Day(models.Model):
    date = models.DateField(
        verbose_name=pgettext_lazy('Business days', 'Day date'),
        unique=True
    )
    is_holiday = models.BooleanField(
        verbose_name=pgettext_lazy('Business days', 'Is holiday'),
        help_text=pgettext_lazy(
            'Business days', 'Either it\'s a holiday or working day'
        ),
        default=True
    )
    is_repeated = models.BooleanField(
        verbose_name=pgettext_lazy('Business days', 'Use every year'),
        help_text=pgettext_lazy(
            'Business days', 'Either use this date every year or only once'
        ),
        default=True
    )

    objects = DayQuerySet().as_manager()

    class Meta:
        verbose_name = pgettext_lazy('Business days', 'Business day')
        verbose_name = pgettext_lazy('Business days', 'Business days')
        ordering = ['-date']

    def __str__(self) -> str:
        return self.date.isoformat()
