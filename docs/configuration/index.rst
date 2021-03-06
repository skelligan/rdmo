Configuration
=============

The RDMO application uses the `Django settings <https://docs.djangoproject.com/en/1.10/topics/settings>`_ module for it's configuration. To seperate the base configuration and your local adjustments and secret information (e.g. database connections), RDMO splits the settings into two files:

* ``rdmo/settings/base.py``, which is part of the git repository and maintained by the RDMO development team.
* ``rdmo/settings/local.py``, which is ignored by git and should be edited by you.

As part of the installation ``rdmo/settings/local.py`` should be creted from the template ``rdmo/settings/sample.local.py``.

While technically the local settings file ``rdmo/settings/local.py`` can be used to override all of the settings in ``rdmo/settings/sample.local.py``, it should be used to customize the settings already available in ``rdmo/settings/sample.local.py``.

This comprises :doc:`general settings <general>`, :doc:`database connections <databases>`, how to send :doc:`emails <email>`, the different :doc:`authentication methods <authentication/index>`, the usage of :doc:`themes <themes>`, and :doc:`caches <cache>`.

.. toctree::
   :maxdepth: 2

   general
   databases
   email
   authentication/index
   themes
   cache
