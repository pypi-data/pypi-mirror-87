
class zwInterface:
    """Representation of a Z-Wave Command Class as an interface."""
    CMD_BASIC_SETUP = 1
    CMD_BASIC_ACTIVE_GET = 2
    CMD_BASIC_PASSIVE_GET = 3
    CMD_BASIC_SET = 4

    def __init__(self, zware, desc, type_id, name, virtual_version, real_if_version, secure, unsecure):
        """Initialize a z-wave Command Class as an interface."""
        self.zware = zware

        # Properties of an interface.
        self.id = desc
        self.type_id = type_id
        self.name = name
        self.virtual_version = virtual_version
        self.real_version = real_if_version
        self.secure = (int(secure) == 1)
        self.unsecure = (int(unsecure) == 1)

        self.status = None

    def send_command(self, cmd, arg='', dev='basic'):
        """
        Send a command to an interface.
        Override this function for each specific Command Class.
        """
        self.zware.zw_api('zwif_' + dev, 'cmd={}&ifd={}'.format(cmd, self.id) + arg)

    def ret_command(self, cmd, arg='', dev='basic'):
        """
        Send a command to an interface that returns data.
        Override this function for each specific Command Class.
        """
        r = self.zware.zw_api('zwif_' + dev, 'cmd={}&ifd={}'.format(cmd, self.id) + arg)
        if cmd == self.CMD_BASIC_ACTIVE_GET or cmd == self.CMD_BASIC_PASSIVE_GET:
            return r.find('./zwif/' + dev)
        return r
