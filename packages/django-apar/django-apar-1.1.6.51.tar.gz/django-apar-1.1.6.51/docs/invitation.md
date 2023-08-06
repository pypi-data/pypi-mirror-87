=====
User
=====

Quick start
-----------

1. Add "users" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'aparnik.contrib.invitation',
    ]

2. Include the users URLconf in your project urls.py like this::

    url(r'^invite/', include('aparnik.contrib.invitation.api.urls', namespace='invite')),

3. Run `python manage.py migrate`.

4. Add config to settings if you want:

    APARNIK = {
        ....
        'INVITATION_PERCENT_DISCOUNT': 10,
        ....
    }