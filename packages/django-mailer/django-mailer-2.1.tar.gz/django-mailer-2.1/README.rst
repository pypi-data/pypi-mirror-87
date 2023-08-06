Django Mailer
-------------

.. image:: http://slack.pinaxproject.com/badge.svg
   :target: http://slack.pinaxproject.com/

.. image:: https://img.shields.io/travis/pinax/django-mailer.svg
    :target: https://travis-ci.org/pinax/django-mailer

.. image:: https://img.shields.io/coveralls/pinax/django-mailer.svg
    :target: https://coveralls.io/r/pinax/django-mailer

.. image:: https://img.shields.io/pypi/dm/django-mailer.svg
    :target:  https://pypi.python.org/pypi/django-mailer/

.. image:: https://img.shields.io/pypi/v/django-mailer.svg
    :target:  https://pypi.python.org/pypi/django-mailer/

.. image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target:  https://pypi.python.org/pypi/django-mailer/


django-mailer
-------------

``django-mailer`` is a reusable Django app for queuing the sending of email.
It works by storing email in the database for later sending.

Keep in mind that file attachments are also temporarily stored in the database, which means if you are sending files larger than several hundred KB in size, you are likely to run into database limitations on how large your query can be. If this happens, you'll either need to fall back to using Django's default mail backend, or increase your database limits (a procedure that depends on which database you are using).

django-mailer was developed as part of the `Pinax ecosystem <http://pinaxproject.com>`_ but is just a Django app and can be used independently of other Pinax apps.


Requirements
------------

* Django >= 1.11

* Databases: django-mailer supports all databases that Django supports, with the following notes:

  * SQLite: you may experience 'database is locked' errors if the ``send_mail``
    command runs when anything else is attempting to put items on the queue. For this reason
    SQLite is not recommended for use with django-mailer.



Getting Started
---------------

Simple usage instructions:

In ``settings.py``:
::

    INSTALLED_APPS = [
        ...
        "mailer",
        ...
    ]

    EMAIL_BACKEND = "mailer.backend.DbBackend"

Run database migrations to set up the needed database tables.

Then send email in the normal way, as per the `Django email docs <https://docs.djangoproject.com/en/stable/topics/email/>`_, and they will be added to the queue.

To actually send the messages on the queue, add this to a cron job file or equivalent::

    *       * * * * (/path/to/your/python /path/to/your/manage.py send_mail >> ~/cron_mail.log 2>&1)
    0,20,40 * * * * (/path/to/your/python /path/to/your/manage.py retry_deferred >> ~/cron_mail_deferred.log 2>&1)

To prevent from the database filling up with the message log, you should clean it up every once in a while.

To remove successful log entries older than a week, add this to a cron job file or equivalent::

    0 0 * * * (/path/to/your/python /path/to/your/manage.py purge_mail_log 7 >> ~/cron_mail_purge.log 2>&1)

Use the `-r failure` option to remove only failed log entries instead, or `-r all` to remove them all.

Documentation and support
-------------------------

See `usage.rst <https://github.com/pinax/django-mailer/blob/master/docs/usage.rst#usage>`_
in the docs for more advanced use cases.
The Pinax documentation is available at http://pinaxproject.com/pinax/.

This is an Open Source project maintained by volunteers, and outside this documentation the maintainers
do not offer other support. For cases where you have found a bug you can file a GitHub issue.
In case of any questions we recommend you join the `Pinax Slack team <http://slack.pinaxproject.com>`_
and ping the Pinax team there instead of creating an issue on GitHub. You may also be able to get help on
other programming sites like `Stack Overflow <https://stackoverflow.com/>`_.


Contribute
----------

See `CONTRIBUTING.rst <https://github.com/pinax/django-mailer/blob/master/CONTRIBUTING.rst>`_ for information about contributing patches to ``django-mailer``.

See this `blog post including a video <http://blog.pinaxproject.com/2016/02/26/recap-february-pinax-hangout/>`_, or our `How to Contribute <http://pinaxproject.com/pinax/how_to_contribute/>`_ section for an overview on how contributing to Pinax works. For concrete contribution ideas, please see our `Ways to Contribute/What We Need Help With <http://pinaxproject.com/pinax/ways_to_contribute/>`_ section.


We also highly recommend reading our `Open Source and Self-Care blog post <http://blog.pinaxproject.com/2016/01/19/open-source-and-self-care/>`_.


Code of Conduct
---------------

In order to foster a kind, inclusive, and harassment-free community, the Pinax Project has a `code of conduct <http://pinaxproject.com/pinax/code_of_conduct/>`_.
We ask you to treat everyone as a smart human programmer that shares an interest in Python, Django, and Pinax with you.



Pinax Project Blog and Twitter
------------------------------

For updates and news regarding the Pinax Project, please follow us on Twitter at @pinaxproject and check out `our blog <http://blog.pinaxproject.com>`_.
