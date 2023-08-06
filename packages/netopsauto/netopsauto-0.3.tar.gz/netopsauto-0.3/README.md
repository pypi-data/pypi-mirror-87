# NetOpsAuto : Automation Module For Network Switches

NetOpsAuto (netopsauto) is a lightweight automation package for Juniper switches using the [Juniper PyEZ][] Python library.

Expansion for Aruba Network Switch automation is a possiblility in the future.

## Documentation

NetOpsAuto's documentation is located at <https://netopsauto.readthedocs.io/>

## Installation

NetOpsAuto suppoorts Python 3.85+. The reccomended way of installing the module is via pip:
``` sh
pip install netopsauto
```

You can also clone the [git repository][] and run the setup.py in a new virtual environment.
Create new virtual environment within the netopsauto repository:

``` sh
python -m venv env
```

Activate the virtual environment:

``` sh
./env/Scripts/Activate.ps1
```

To install the package, run the `setup.py`:

``` sh
pip install ./
```

If you encounter any errors installing through pip, update by running `python -m pip install --upgrade pip` and try again.

## Installing Through GitHub

You can also directly clone a copy of the repository using git, like so:

``` sh
pip install --upgrade git+https://github.com/dmtx97/netopsauto
```

## Usage

If you cloned the repository, the `cli.py` script provides an example implementation of the module with command line arguments. It is also advised to create a switch schema similar to the one provided in [data/input/switches-example.json][].

  [Juniper PyEZ]: https://github.com/Juniper/py-junos-eznc
  [git repository]: https://github.com/dmtx97/netopsauto.git
  [data/input/switches-example.json]: https://github.com/dmtx97/netopsauto/blob/master/data/input/switches-example.json
  
### Module Completion
[X] Juniper Network Instance
[X] Secure access port automation change
[X] Automate Rescue Configurations
[ ] Add SNMP Automation Script
[ ] Complete password change function
[ ] Aruba Switch Instance
  
  