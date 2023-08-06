Installation
============

.. toctree::
   :maxdepth: 1

   
NetOpsAuto suppoorts Python 3.85+. The recommended way to clone the `git repository <https://github.com/dmtx97/netopsauto.git>`_ and run the setup.py in a new virtual environment.


Create new virtual environment within the netopsauto repository:

.. code-block:: sh

   python -m venv env

Activate the virtual environment:

.. code-block:: sh

   ./env/Scripts/Activate.ps1

To install the package, run the :code:`setup.py`:

.. code-block:: sh

   pip install ./

.. note::
   If you encounter any errors installing through pip, update by running :code:`python -m pip install --upgrade pip` and try again.


Installing Through GitHub
^^^^^^^^^^^^^^^^^^^^^^^^^

You can also directly clone a copy of the repository using git, like so:

.. code-block:: sh

   pip install --upgrade git+https://github.com/dmtx97/netopsauto
