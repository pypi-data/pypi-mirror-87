from . import zwInterface


class zwBattery(zwInterface):
    """Representation of a Z-Wave Battery Command Class."""
    CMD_BATTERY_ACTIVE_GET = 2
    CMD_BATTERY_PASSIVE_GET = 3

    def send_command(self, cmd, arg='', dev='battery'):
        """Send a command to the Battery Command Class."""
        super().send_command(cmd, arg=arg, dev=dev)

    def ret_command(self, cmd, arg='', dev='battery'):
        """Send a command to the Battery Command Class that returns data."""
        return super().ret_command(cmd, arg=arg, dev=dev)

    def get_status(self, active=False):
        """Get the battery level of the lock."""
        cmd = self.CMD_BATTERY_ACTIVE_GET if active else self.CMD_BATTERY_PASSIVE_GET
        status = self.ret_command(cmd)
        self.status = int(status.get('level'))
        return {'battery': self.status}