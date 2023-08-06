from django.contrib import admin

from .models import Day


@admin.register(Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'is_holiday', 'is_repeated']
    list_editable = ['date', 'is_holiday', 'is_repeated']
    list_filter = ['date', 'is_holiday', 'is_repeated']
