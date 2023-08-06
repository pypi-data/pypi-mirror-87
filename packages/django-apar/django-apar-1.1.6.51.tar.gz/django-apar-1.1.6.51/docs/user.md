=====
User
=====

Quick start
-----------

1. Add "users" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'aparnik.contrib.users',
    ]

2. Include the users URLconf in your project urls.py like this::

    url(r'^user/', include('aparnik.contrib.user.api.urls', namespace='user')),

3. Run `python manage.py migrate`.

4. Add config to settings if you want:

    APARNIK = {
        ....
        'USER_LOGIN_WITH_PASSWORD': False,
        'USER_CREATE_SERIALIZER': 'aparnik.contrib.users.api.serializers.UserCreateSerializer',
        'USER_UPDATE_SERIALIZER': 'aparnik.contrib.users.api.serializers.UserUpdateSerializer',
        'USER_DETAIL_SERIALIZER': 'aparnik.contrib.users.api.serializers.UserDetailSerializer',
        'USER_SUMMARY_LIST_SERIALIZER': 'aparnik.contrib.users.api.serializers.UserSummaryListSerializer',
        'USER_LOGIN_API_VIEW': 'aparnik.contrib.users.api.views.UserLoginAPI',
        'USER_LIST_API_VIEW': 'aparnik.contrib.users.api.views.UserListAPIView',
        'USER_DETAIL_API_VIEW': 'aparnik.contrib.users.api.views.UserDetailAPIView',
        'USER_CREATE_API_VIEW': 'aparnik.contrib.users.api.views.UserCreateAPIView',
        'USER_UPDATE_API_VIEW': 'aparnik.contrib.users.api.views.UserUpdateAPIView',
        'USER_INVITATION_CODE_LENGTH': 6,
        'USER_INVITATION_CODE_INT': False,
        'USER_IS_SHOW_ADMIN_PANEL': True,
        'USER_REGISTER_WITH_LOGIN': False,
        'SMS_EXPIRE_TOKEN': 120,
        'SMS_API_KEY': '',
        'SMS_OTA_NAME': '',
        'SEND_SMS': False,
        'VERIFY_FAKE': False,
        'VERIFY_FAKE_CODE': '1111',
        'JALALI_FORMAT': '%Y/%m/%d',
        ....
    }

    # User
    AUTH_USER_MODEL = 'aparnik_users.User'
    AUTHENTICATION_BACKENDS = ('aparnik.contrib.users.backends.AuthBackend', 'django.contrib.auth.backends.ModelBackend')