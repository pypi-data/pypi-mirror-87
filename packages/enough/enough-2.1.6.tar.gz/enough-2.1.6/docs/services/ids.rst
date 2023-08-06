.. _ids:

Intrusion Detection System
==========================

The `Wazuh <http://wazuh.com/>`_ Intrusion Detection System watches
over all hosts and will report problems to the `ids@example.com` mail
address.

The service is created on the host specified by the `--host` argument:

.. code::

    $ enough --domain example.com service create --host wazuh-host wazuh
