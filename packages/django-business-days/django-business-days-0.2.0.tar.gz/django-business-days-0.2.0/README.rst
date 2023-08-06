
django-business-days
====================

Wrapper around `business-python <https://pypi.org/project/business-python/>`_ with days in your admin.

Installation
------------

``$ pip install django-business-days``

Add ``django_business_days`` to ``INSTALLED_APPS``

How to use it
-------------

.. code-block:: python

   from django_business_days.calendar import get_calendar
   from datetime import timedelta

   # Note: django applications must be ready, because
   # queries are made during initialization
   calendar = get_calendar()

   # Next just use class-API from `business-python`
   calendar.is_business_day("Monday, 8 June 2020")

   input_date = Calendar.parse_date("Saturday, 14 June 2014")
   calendar.business_days_between(input_date, input_date + timedelta(days=7))

TODO:
-----


* Add tests
