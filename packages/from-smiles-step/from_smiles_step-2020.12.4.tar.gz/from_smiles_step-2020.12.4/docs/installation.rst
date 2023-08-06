.. highlight:: shell

============
Installation
============

Note: It is possible that under MacOS you need to have gfortran installed in order to have the runtime
libraries needed from some aspects of OpenBabel to function properly. This needs to be checked more
carefully, but it seemd that creating structures from SMILES functioned, but gave structures with
atoms close to each other until gfotran was installed.

Stable release
--------------

To install From SMILES step, run this command in your terminal:

.. code-block:: console

    $ pip install from_smiles_step

This is the preferred method to install From SMILES step, as it will always install the most recent stable release. 

If you don't have `pip`_ installed, this `Python installation guide`_ can guide
you through the process.

.. _pip: https://pip.pypa.io
.. _Python installation guide: http://docs.python-guide.org/en/latest/starting/installation/


From sources
------------

The sources for From SMILES step can be downloaded from the `Github repo`_.

You can either clone the public repository:

.. code-block:: console

    $ git clone git://github.com/paulsaxe/from_smiles_step

Or download the `tarball`_:

.. code-block:: console

    $ curl  -OL https://github.com/paulsaxe/from_smiles_step/tarball/master

Once you have a copy of the source, you can install it with:

.. code-block:: console

    $ python setup.py install


.. _Github repo: https://github.com/paulsaxe/from_smiles_step
.. _tarball: https://github.com/paulsaxe/from_smiles_step/tarball/master
