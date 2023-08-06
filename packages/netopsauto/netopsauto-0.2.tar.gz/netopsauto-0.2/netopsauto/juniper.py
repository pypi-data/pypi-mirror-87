from jnpr.junos.utils.start_shell import StartShell
from jnpr.junos.utils.config import Config
from jnpr.junos import Device
from paramiko import AuthenticationException
from lxml import etree
from xml.etree import ElementTree

class Juniper:
    """A class which implements Juniper Networks PyEZ module.

    Initializes a new instance of a Juniper device.

    :param host_name: host name for Juniper device
    :type host_name: str
    
    :param host_address: host address for Juniper device
    :type host_address: str
    
    :param user: username for Juniper login
    :type user: str
    
    :param password: password for Juniper login
    :type password: str
    
    """

    def __init__(self, host_name, host_address, user, password):
        self.host_address = host_address
        self.user = user
        self.password = password
        self.host_name = host_name

    def initialize_device(self):
        """Initializes new instance of `jnpr.junos.device.Device <https://junos-pyez.readthedocs.io/en/2.5.1/jnpr.junos.html#module-jnpr.junos.device>`_.

        Optionally call this function to utilize the PyEz Device instance directly, otherwise the associated functions provided by the **netopsauto.juniper.Juniper** class will initialize a Device object for you.

        :return: `jnpr.junos.device.Device <https://junos-pyez.readthedocs.io/en/2.5.1/jnpr.junos.html#module-jnpr.junos.device>`_ 
        """
        dev = Device(host = self.host_address, user = self.user, password = self.password)
        return dev

    def get_enabled_interfaces(self):
        """ 
        :return: list of Physical Interfaces which read :code:`Enabled, Physical link is Down`
        :rtype: list
        """
        dev = self.initialize_device()
        ss = StartShell(dev)
        ss.open()
        cmd = ss.run('cli -c "show interfaces | match Physical | no-more"')
        ss.close()

        enabled_interfaces = []
        unchecked_interfaces = ['ae0', 'ae1', 'ae2', 'ae3', 'ae4', 'me0', 'vme']
        for line in cmd[1].splitlines():
            if "Enabled, Physical link is Down" in line:
                val = line.split("Physical interface: ")[1]
                val = val.split(", Enabled, Physical link is Down")[0]
                if val not in unchecked_interfaces:
                    enabled_interfaces.append(val + '.0')

        return enabled_interfaces

    def get_secure_access_port_status(self, port = None):
        """Generates dictionary of ports and their secure-access-port status for the given Juniper instance. 

        :param port: Port number (0-47 or 0-23) for the current Juniper instance
        :type port: int, optional

        :return: Dictionary of ports with and their ethernet-switching-options status (active or inactive). 
        :rtype: dict
        
        .. note::
            If the **port** parameter is filled, the function will return the status of the individual port.
        
        """

        dev = self.initialize_device()
        dev.open()
        filter = '<configuration><ethernet-switching-options/></configuration>'
        
        data = dev.rpc.get_config(filter_xml=filter)
        xml = etree.tostring(data, encoding='unicode', pretty_print=True)
        dom = ElementTree.fromstring(xml)

        ethernet_status = dom.findall('ethernet-switching-options/secure-access-port/interface')

        interface_to_status = {}
        if port is not None:
            port_query = 'ge-0/0/{}.0'.format(port)
            for i in ethernet_status:
                if i.find("name").text == port_query:
                    if 'inactive' not in i.attrib.keys():
                        interface_to_status[port_query] = 'active'
                    else:
                        interface_to_status[port_query] = 'inactive'
                    break
        else:
            for i in ethernet_status:
                if 'inactive' not in i.attrib.keys():
                    interface_to_status[i.find("name").text] = "active"
                else:
                    interface_to_status[i.find("name").text] = "inactive"

        return interface_to_status

    def activate_port_security(self, port_list):
        """Activates `secure-access-port <https://www.juniper.net/documentation/en_US/junos/topics/reference/configuration-statement/secure-access-port-port-security.html>`_ option for the list of specified ports for the current Juniper instance.
        
        :param port_list: List of desired ports to have secure-access-port enabled
        :type port_list: list
        
        """
        print("Connecting to : {}".format(self.host_name))
        device = self.initialize_device().open()
        cu = Config(device)

        for port in port_list:
            try:
                print("Activating security on port {}".format(port))
                set_command = 'activate ethernet-switching-options secure-access-port interface {}'.format(port)
                cu.load(set_command, format='set')

                if(cu.commit_check()):
                    cu.commit()

            except Exception as e:
                print(e)
                pass

        device.close()
        
    def change_password(self, user, password):
        """Will hash inputted password for new user login for the current Juniper instance.

        :param user: New desired username for login
        :type user: str
        
        :param password: New desired password for login
        :type password: str 
        """

        print("Connecting to : {}".format(self.host_name))
        device = self.initialize_device().open()
        cu = Config(dev)
        print("Changing password...")
        set_command = 'set system login user {} authentication encrypted-password {}'.format(user, password)
        cu.load(set_command, format='set')
        
        if(cu.commit_check()):
            cu.commit()
            print("Password has been changed")
        else:
            print("There is an issue changing the password on this device. Please try again.")
        
        device.close()

    def set_rescue_config(self):
        """Runs the :code:`request system configuration rescue save` command for the current Juniper instance
        """
        dev = self.initialize_device()
        ss = StartShell(dev)
        ss.open()
        print("Setting rescue configuration for {}".format(self.host_name))
        cmd = ss.run('cli -c "request system configuration rescue save"')
        ss.close()
