Django Session Header: Identify the session through a header
============================================================

There are some situations where the browser
may not allow any cookies at all to be used.
In those cases, we would like to be able to fall back
to something that is both secure, and capable.
This package allows you to manually pass the
sessionid using a header, so that you can continue
to use Django's excellent session management.

It extends Django's built-in sessions to support
sessions in places where cookies are not allowed.
For most views, the handling will be seamless.
Those that need to have sessions that persist despite the
absence of cookies, there are a few extra features.


Usage
=====

First, install the package.

.. code-block:: sh

    pip install django-session-header

Replace ``django.contrib.sessions.middleware.SessionMiddleware``
in your ``settings.py`` with the following:

.. code-block:: python

    MIDDLEWARE_CLASSES = [
       # ...
       # 'django.contrib.session.middleware.SessionMiddleware',
       'django_session_header.middleware.SessionMiddleware',
    ]

And replace the Django Rest Framework ``SessionAuthentication``
class with ``django_session_header.authentication.SessionAuthentication``:

.. code-block:: python

    REST_FRAMEWORK = {
        'DEFAUlT_AUTHENTICATION_CLASSES': [
            # ...
            # 'rest_framework.authentication.SessionAuthentication',
            'django_session_header.authentication.SessionAuthentication',
        ]
    }

If a session was obtained via a session header,
then ``request.session.csrf_exempt`` will be ``True``.
You can use this to conditionally apply CSRF protection.
Or, if you prefer, you can replace Django's normal CSRF middleware
with ``django_session_header.middleware.CsrfViewMiddleware``:

.. code-block:: python

    MIDDLEWARE_CLASSES = [
        # ...
        # 'django.middleware.csrf.CsrfViewMiddleware',
        'django_session_header.middleware.CsrfViewMiddleware',
    ]

The ``sessionid`` will be available in the ``X-SessionID`` response header,
and you can now set the ``X-SessionID`` header on the request manually
to avoid needing cookies to power your sessions.
