Getting it
==========

By the time you read this, ``rjgtoys-{{project.id}}`` should be available on PyPi::

    pip install --user rjgtoys-{{project.id}}

To get the source code::

    git clone {{github.base}}{{project.family}}-{{project.name}}.git

To make the package available for your Python::

    cd {{project.family}}-{{project.name}}
    python ./setup.py develop --user

If you are using a virtualenv, you should omit the ``--user`` option used
in these examples.

