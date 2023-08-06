=====
dnoticias_backoffice
=====

dnoticias_backoffice is a Django app to make the authentication in the DNOTICIAS PLATFORMS.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "dnoticias_backoffice" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'dnoticias_backoffice',
    ]

2. Include the dnoticias_backoffice URLconf in your project urls.py like this::

    path('auth/', include('dnoticias_backoffice.urls')),

3. Run ``python manage.py migrate`` to create the polls models.

4. Add the necessary settings variables