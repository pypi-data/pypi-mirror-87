=====
dnoticias_auth
=====

dnoticias_auth is a Django app to make the authentication in the DNOTICIAS PLATFORMS.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "polls" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dnoticias_auth',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('auth/', include('dnoticias_auth.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Add the necessary settings variables