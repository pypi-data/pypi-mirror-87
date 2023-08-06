import urllib3
import zware_api.interfaces as interfaces

from .const import DEVICE_DATABASE

COMMAND_CLASSES = {
    "76": interfaces.zwLockLogging,
    "78": interfaces.zwScheduleEntry,
    "98": interfaces.zwLock,
    "99": interfaces.zwUserCode,
    "113": interfaces.zwAlarm,
    "128": interfaces.zwBattery,
}


class zwClient(object):
    """Representation of a Z-Wave network client."""
    CMD_ADD_NODE = 2
    CMD_DELETE_NODE = 3

    def __init__(self, zware_object, host, user, password):
        """Initialize a z-wave client."""
        urllib3.disable_warnings()
        self.zware = zware_object
        self.ipAddress = host
        self.username = user
        self.password = password
        self.nodes = list()

    def login(self):
        """Connect to the server"""
        board_ip = 'https://' + self.ipAddress + '/'
        r = self.zware.zw_init(board_ip, self.username, self.password)
        v = r.findall('./version')[0]
        return v.get('app_major') + '.' + v.get('app_minor')

    def get_node_list(self, active=False):
        """Get nodes in the z-wave network."""
        if active:
            nodes_list = list()
            nodes = self.zware.zw_api('zwnet_get_node_list')
            nodes = nodes.findall('./zwnet/zwnode')
            for node in nodes:
                node_obj = zwNode(self.zware, node.get('id'), node.get('property'), node.get('vid'),
                                  node.get('pid'), node.get('type'), node.get('category'),
                                  node.get('alive'), node.get('sec'))
                nodes_list.append(node_obj)
            self.nodes = nodes_list
        return self.nodes

    def add_node(self):
        """Activate adding mode in a Z-Wave network."""
        self.zware.zw_add_remove(self.CMD_ADD_NODE)
        self.zware.zw_net_comp(self.CMD_ADD_NODE)

    def remove_node(self):
        """Activate exclusion mode in a Z-Wave network."""
        self.zware.zw_add_remove(self.CMD_DELETE_NODE)
        self.zware.zw_net_comp(self.CMD_DELETE_NODE)

    def cancel_command(self):
        """Cancel the last sent Z-Wave command."""
        self.zware.zw_abort()


class zwNode:
    """Representation of a Z-Wave Node."""

    def __init__(self, zware, id, property, manufacturer_id, product_id, product_type,
                 device_category, alive_state, is_secure):
        """Initialize a z-wave node."""
        self.zware = zware

        # Properties of a z-wave node.
        self.id = id
        self.property = property
        self.manufacturer_id = manufacturer_id
        self.product_id = product_id
        self.product_type = product_type
        self.device_category = device_category
        self.alive_state = alive_state
        self.is_secure = (int(is_secure) == 1)

        self.endpoints = list()
        self.name = None
        self.location = None

    def get_name_and_location(self, active=False):
        """Get the current name and location of a node."""
        if active:
            endpoints = self.zware.zw_api('zwnode_get_ep_list', 'noded=' + self.id)
            endpoints = endpoints.findall('./zwnode/zwep')
            self.name = endpoints[0].get('name', '').replace("%20", " ")
            self.location = endpoints[0].get('loc').replace("%20", " ")
        return self.name, self.location

    def set_node_name_and_location(self, name, location):
        """Set the name and location of a node."""
        if len(self.endpoints) == 0:
            self.get_endpoints(active=True)
        self.zware.zw_nameloc(self.endpoints[0].id, name, location)
        self.name = name
        self.location = location

    def get_readable_manufacturer_model(self):
        """Return a tupple with human-readable device manufacturer and model"""
        return (DEVICE_DATABASE.get(self.manufacturer_id, {}).get("name"),
                DEVICE_DATABASE.get(self.manufacturer_id, {}).get(
                    "product",{}).get(self.product_id, {}).get(self.product_type))

    def send_nif(self):
        """Send a node information frame to the node."""
        self.zware.zw_api('zwnet_send_nif', 'noded=' + self.id)
        self.zware.zw_net_wait()

    def update(self):
        """Update the node status in the zwave network."""
        self.zware.zw_api('zwnode_update', 'noded=' + self.id)
        self.zware.zw_net_wait()

    def get_endpoints(self, active=False):
        """Get endpoints in a z-wave node."""
        if active:
            ep_list = list()
            endpoints = self.zware.zw_api('zwnode_get_ep_list', 'noded=' + self.id)
            endpoints = endpoints.findall('./zwnode/zwep')
            for ep in endpoints:
                ep_obj = zwEndpoint(self.zware, ep.get('desc'), ep.get('generic'), ep.get('specific'),
                                    ep.get('name'), ep.get('loc'), ep.get('zwplus_ver'),
                                    ep.get('role_type'), ep.get('node_type'), ep.get('instr_icon'),
                                    ep.get('usr_icon'))
                ep_list.append(ep_obj)
            self.endpoints = ep_list
        return self.endpoints


class zwEndpoint:
    """Representation of a Z-Wave Endpoint."""

    def __init__(self, zware, id, generic, specific, name, location, version, role_type,
                 node_type, instr_icon, user_icon):
        """Initialize a z-wave endpoint."""
        self.zware = zware

        # Properties of a z-wave endpoint.
        self.id = id
        self.generic = generic
        self.specific = specific
        self.name = name
        self.location = location
        self.zw_plus_version = version
        self.role_type = role_type
        self.node_type = node_type
        self.installer_icon = instr_icon
        self.user_icon = user_icon

        self.interfaces = list()

    def get_interfaces(self, active=False):
        """Get all the interfaces of an endpoint."""
        if active:
            if_list = list()
            itfs = self.zware.zw_api('zwep_get_if_list', 'epd=' + self.id)
            itfs = itfs.findall('./zwep/zwif')
            for itf in itfs:
                type_id = itf.get('id')
                if_obj = COMMAND_CLASSES.get(type_id,
                                             interfaces.zwInterface)(self.zware, itf.get('desc'), type_id,
                                                                     itf.get('name'), itf.get('ver'),
                                                                     itf.get('real_ver'),
                                                                     itf.get('sec'), itf.get('unsec'))
                if_list.append(if_obj)
            self.interfaces = if_list
        return self.interfaces
