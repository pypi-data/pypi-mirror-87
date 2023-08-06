=====
Usage
=====

First, add "mailer" to your ``INSTALLED_APPS`` in your settings.py.
Run ``./manage.py migrate`` to install models.

Using EMAIL_BACKEND
===================

This is the preferred and easiest way to use django-mailer.

To automatically switch all your mail to use django-mailer, first set
EMAIL_BACKEND::

    EMAIL_BACKEND = "mailer.backend.DbBackend"

If you were previously using a non-default EMAIL_BACKEND, you need to configure
the MAILER_EMAIL_BACKEND setting, so that django-mailer knows how to actually send
the mail::

    MAILER_EMAIL_BACKEND = "your.actual.EmailBackend"

Now, just use the normal `Django mail functions
<https://docs.djangoproject.com/en/stable/topics/email/>`_ for sending email. These
functions will store mail on a queue in the database, which must be sent as
below.

Explicitly putting mail on the queue
====================================

If you don't want to send all email through django-mailer, you can send mail
using ``mailer.send_mail``, which has the same signature as Django's
``send_mail`` function.

You can also do the following::

    # favour django-mailer but fall back to django.core.mail
    from django.conf import settings

    if "mailer" in settings.INSTALLED_APPS:
        from mailer import send_mail
    else:
        from django.core.mail import send_mail

and then just call send_mail like you normally would in Django::

    send_mail(subject, message_body, settings.DEFAULT_FROM_EMAIL, recipients)

There is also a convenience function ``mailer.send_html_mail`` for creating HTML
(this function is **not** in Django)::

    send_html_mail(subject, message_plaintext, message_html, settings.DEFAULT_FROM_EMAIL, recipients)

Additionally you can send all the admins as specified in the ``ADMIN``
setting by calling::

    mail_admins(subject, message_body)

or all managers as defined in the ``MANAGERS`` setting by calling::

    mail_managers(subject, message_body)

Clear queue with command extensions
===================================

With mailer in your INSTALLED_APPS, there will be three new manage.py commands
you can run:

* ``send_mail`` will clear the current message queue. If there are any
  failures, they will be marked deferred and will not be attempted again by
  ``send_mail``.

* ``retry_deferred`` will move any deferred mail back into the normal queue
  (so it will be attempted again on the next ``send_mail``).

* ``purge_mail_log`` will remove old successful message logs from the database, to prevent it from filling up your database.
  Use the ``-r failure`` option to remove only failed message logs instead, or ``-r all`` to remove them all.


You may want to set these up via cron to run regularly::


    *       * * * * (/path/to/your/python /path/to/your/manage.py send_mail >> ~/cron_mail.log 2>&1)
    0,20,40 * * * * (/path/to/your/python /path/to/your/manage.py retry_deferred >> ~/cron_mail_deferred.log 2>&1)
    0 0 * * * (/path/to/your/python /path/to/your/manage.py purge_mail_log 7 >> ~/cron_mail_purge.log 2>&1)

For use in Pinax, for example, that might look like::

    * * * * * (cd $PINAX; /usr/local/bin/python2.5 manage.py send_mail >> $PINAX/cron_mail.log 2>&1)
    0,20,40 * * * * (cd $PINAX; /usr/local/bin/python2.5 manage.py retry_deferred >> $PINAX/cron_mail_deferred.log 2>&1)
    0 0 * * * (cd $PINAX; /usr/local/bin/python2.5 manage.py purge_mail_log 7 >> $PINAX/cron_mail_purge.log 2>&1)

This attempts to send mail every minute with a retry on failure every 20
minutes, and purges the mail log for entries older than 7 days.

``manage.py send_mail`` uses a lock file in case clearing the queue takes
longer than the interval between calling ``manage.py send_mail``.

Note that if your project lives inside a virtualenv, you also have to execute
this command from the virtualenv. The same, naturally, applies also if you're
executing it with cron. The `Pinax documentation`_ explains that in more
details.

.. _pinax documentation: http://pinaxproject.com/docs/dev/deployment.html#sending-mail-and-notices

Controlling the delivery process
================================

If you wish to have a finer control over the delivery process, which defaults
to deliver everything in the queue, you can use the following 3 variables
(default values shown)::

    MAILER_EMAIL_MAX_BATCH = None  # integer or None
    MAILER_EMAIL_MAX_DEFERRED = None  # integer or None
    MAILER_EMAIL_THROTTLE = 0  # passed to time.sleep()

These control how many emails are sent successfully before stopping the
current run `MAILER_EMAIL_MAX_BATCH`, after how many failed/deferred emails
should it stop `MAILER_EMAIL_MAX_DEFERRED` and how much time to wait between
each email `MAILER_EMAIL_THROTTLE`.

Unprocessed emails will be evaluated in the following delivery iterations.

Error handling
==============

django-mailer comes with a default error handler
``mailer.engine.handle_delivery_exception``.

It marks the related message as deferred for any of these exceptions:

- ``smtplib.SMTPAuthenticationError``
- ``smtplib.SMTPDataError``
- ``smtplib.SMTPRecipientsRefused``
- ``smtplib.SMTPSenderRefused``
- ``socket.error``

Any other exceptions is re-raised.
That is done for backwords-compatiblity as well as for flexibility:
we would otherwise have to maintain an extensive and changing
list of exception types, which does not scale, and you get
the chance to do error handling that fits your environment like a glove.

When the default behavior does not fit your environment, you can specify your
own custom delivery error handler through setting ``MAILER_ERROR_HANDLER``.
The value should be a string for use with Django's ``import_string``,
the default is ``"mailer.engine.handle_delivery_exception"``.

Your handler is passed three arguments, in order:

- ``connection`` — the backend connection instance that failed delivery
- ``message`` — the ``Message`` instance that failed delivery
- ``exc`` — the exception instance raised by the mailer backend

Your handler should return a 2-tuple of:

1. a connection instance (or ``None`` to cause a new connection to be created)
2. a string denoting the action taken by the handler,
   either ``"sent"`` or ``"deferred"`` precisely

For an example of a custom error handler::

    def my_handler(connection, message, exc):
        if isinstance(exc, SomeDeliveryException):
            # trying to re-send this very message desparately
            # (if you have good reason to)
            [..]
            status = 'sent'
        elif isinstance(exc, SomeOtherException):
            message.defer()
            connection = None  # i.e. ask for a new connection
            status = 'deferred'
        else:
            six.reraise(*sys.exc_info())

        return connection, status

Other settings
==============

If you need to be able to control where django-mailer puts its lock file (used
to ensure mail is not sent twice), you can set ``MAILER_LOCK_PATH`` to a full
absolute path to the file to be used as a lock. The extension ".lock" will be
added. The process running ``send_mail`` needs to have permissions to create and
delete this file, and others in the same directory. With the default value of
``None`` django-mailer will use a path in current working directory.

If you need to disable the file-based locking, you can set the
``MAILER_USE_FILE_LOCK`` setting to ``False``.

If you need to change the batch size used by django-mailer to save messages in
``mailer.backend.DbBackend``, you can set ``MAILER_MESSAGES_BATCH_SIZE`` to a
value more suitable for you. This value, which defaults to `None`, will be passed to
`Django's bulk_create method <https://docs.djangoproject.com/en/stable/ref/models/querysets/#bulk-create>`_
as the `batch_size` parameter.

Using the DontSendEntry table
=============================

django-mailer creates a ``DontSendEntry`` model, which is used to filter out
recipients from messages being created.

But beware, it's actually only used when directly sending messages through
mailer, not when mailer is used as an alternate ``EMAIL_BACKEND`` for Django.
Also, even if recipients become empty due to this filtering, the email will be
queued for sending anyway. (A patch to fix these issues would be accepted)
