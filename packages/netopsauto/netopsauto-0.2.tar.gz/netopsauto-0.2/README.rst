NetOpsAuto : Automation Module For Network Switches
==============================================================

NetOpsAuto (netopsauto) is a lightweight automation package for Juniper switches using the `Juniper PyEZ <https://github.com/Juniper/py-junos-eznc>`_ Python library.

Expansion for Aruba Network Switch automation is a possiblility in the future.

Documentation
^^^^^^^^^^^^^

NetOpsAuto's documentation is located at https://netopsauto.readthedocs.io/

Installation
^^^^^^^^^^^^
   
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

If you encounter any errors installing through pip, update by running :code:`python -m pip install --upgrade pip` and try again.

Installing Through GitHub
^^^^^^^^^^^^^^^^^^^^^^^^^

You can also directly clone a copy of the repository using git, like so:

.. code-block:: sh

   pip install --upgrade git+https://github.com/dmtx97/netopsauto

Usage
^^^^^

The :code:`cli.py` script provides an example implementation of the module with command line arguments. It is also recommended to create a switch schema similar to the one provided in `data/input/switches-example.json <https://github.com/dmtx97/netopsauto/blob/master/data/input/switches-example.json>`_. 
