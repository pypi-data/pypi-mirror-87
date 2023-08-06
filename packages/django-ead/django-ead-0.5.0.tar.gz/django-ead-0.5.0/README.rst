==============================
EAD and EAC-CPF Django Package
==============================

.. image:: https://badge.fury.io/py/autharch-base.svg
    :target: https://badge.fury.io/py/autharch-base

.. image:: https://travis-ci.org/kingsdigitallab/autharch-base.svg?branch=master
    :target: https://travis-ci.org/kingsdigitallab/autharch-base

.. image:: https://codecov.io/gh/kingsdigitallab/autharch-base/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kingsdigitallab/autharch-base

Django app supporting EAD3 data import, editing, and XML serialisation.


Documentation
-------------

The full documentation is at https://autharch-base.readthedocs.io.


Quickstart
----------

Install EAD and EAC-CPF Django Package::

    pip install autharch-base

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'ead.apps.EADConfig',
        ...
    )

Add EAD and EAC-CPF Django Package's URL patterns:

.. code-block:: python

    from ead import urls as ead_urls


    urlpatterns = [
        ...
        url(r'^', include(ead_urls)),
        ...
    ]


Features
--------

* Models for almost all of EAD3 (dsc and @entityref unsupported).
* Import script for EAD3 XML.
* Serialisation to EAD3 XML.


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
