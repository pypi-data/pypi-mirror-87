Introduction
============

django-fs-leonid is the Django-related reusable app provides the ability to create and store in a database files such as robots.txt, sitemap.xml and so on.


Installation
============

1. Install ``django-fs-leonid`` using ``pip``::

    $ pip install django-fs-leonid

2. Add ``'fs_leonid'`` to your ``INSTALLED_APPS`` setting::

    INSTALLED_APPS = (
        ...
        'fs_leonid',
        ...
    )

3. Update your ``urls.py``::

    path('', include('fs_leonid.urls')),

4. Run ``migrate``::

    $ ./manage.py migrate


Credits
=======

`Fogstream <https://fogstream.ru>`_
