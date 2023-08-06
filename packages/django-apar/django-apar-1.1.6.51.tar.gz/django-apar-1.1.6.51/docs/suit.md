=====
User
=====

Quick start
-----------

1. Add "suit" to your INSTALLED_APPS setting like this:

    `‍INSTALLED_APPS = [   
        ...
        'aparnik.contrib.suit',
        'django.contrib.admin',
        ...
        
    ]‍`
    
    **Attention**: add suit before `django.contrib.admin`

2. Include the users URLconf in your project urls.py like this:
    from aparnik.contrib.suit.views import login
    url(r'^admin/login', login),
