=====
Province
=====

Province add province of Iran to your project with city, town, shahrak.


Quick start
-----------

1. Add "province" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'aparnik.contrib.province',
    ]

2. Include the province URLconf in your project urls.py like this::

    url(r'^province/', include('aparnik.contrib.province.api.urls', namespace='province')),

3. Run `python manage.py migrate`.

4. Use it.