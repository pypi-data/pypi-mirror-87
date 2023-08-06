Notes plugin for `Grvlms <https://docs.grvlms.overhang.io>`__
===================================================================================

Installation
------------

::

    pip install git+https://github.com/groovetch/grvlms-notes

Usage
-----

::

    grvlms plugins enable notes
    grvlms notes config -i (variable configuration option)
    grvlms local start

Configuration
-------------

- ``NOTES_MYSQL_PASSWORD`` (default: ``"{{ 8|random_string }}"``)
- ``NOTES_SECRET_KEY`` (default: ``"{{ 24|random_string }}"``)
- ``OAUTH2_KEY`` (default: ``"{{ 8|random_string }}"``)
- ``NOTES_OAUTH2_SECRET`` (default: ``"{{ 24|random_string }}"``)
- ``NOTES_DOCKER_IMAGE`` (default: ``"groovetech/openedx-notes:{{ NOTES_VERSION }}"``)
- ``NOTES_HOST`` (default: ``"notes.{{ WILDCARD_DOMAIN }}"``)
- ``NOTES_MYSQL_DATABASE`` (default: ``"notes"``)
- ``NOTES_MYSQL_USERNAME`` (default: ``"notes"``)
    

License
-------

This software is licensed under the terms of the AGPLv3.