darfix
=========

Darfix is a Python library for the analysis of dark-field microscopy data. It provides a series of computer vision techniques, together with a graphical user interface and an Orange3 (https://github.com/biolab/orange3) add-on to define the workflow.

Installation
------------

To install the last release with all its dependencies run

.. code-block:: bash

    pip install darfix[full]

To install it with a minimal set of dependencies run

.. code-block:: bash

    pip install darfix

To install from sources:

.. code-block:: bash

    git clone https://gitlab.esrf.fr/julia.garriga/darfix.git
    cd darfix
    pip install -r requirements.txt
    pip install .

To test the orange workflow (only from sources) just run

.. code-block:: bash

    orange-canvas orangecontrib/darfix/tutorials/example_tutorial.ows

Documentation
-------------
The documentation of the latest release is available at http://www.edna-site.org/pub/doc/darfix/latest
