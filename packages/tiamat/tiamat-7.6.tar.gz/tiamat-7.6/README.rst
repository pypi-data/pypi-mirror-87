======
TIAMAT
======

*Tiamat is the single binary builder for Python projects.*

Tiamat is the single binary builder for Python-based projects that use pop. Pop
is the implementation of the Plugin Oriented Programming software development
paradigm. For more information about Plugin Oriented Programming and how to
develop in pop, see
`The Intro to Plugin Oriented Programming <https://pop-book.readthedocs.io/>`_.

.. Note::
    While Tiamat is written with the intent of supporting pop projects it can be
    used with any Python project.

Tiamat can be used to define a build without altering the target application's
source tree, which can be useful when building third party applications.

All that needs to be done is to define a ``run.py`` as the entry script and
then to create a ``requirements.txt`` file that will include the target
application.

- Read the `Quickstart Guide <https://gitlab.com/saltstack/pop/tiamat/-/blob/master/docs/topics/quickstart.rst>`_
