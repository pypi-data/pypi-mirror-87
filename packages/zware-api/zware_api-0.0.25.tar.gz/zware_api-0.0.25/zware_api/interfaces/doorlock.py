from . import zwInterface


class zwLock(zwInterface):
    """Representation of a Z-Wave Lock Command Class."""
    CMD_OPEN_DOOR = 0
    CMD_CLOSE_DOOR = 255

    CMD_DLOCK_SETUP = 1
    CMD_DLOCK_OP_ACTIVE_GET = 2
    CMD_DLOCK_OP_PASSIVE_GET = 3
    CMD_DLOCK_OP_SET = 4
    CMD_DLOCK_CFG_ACTIVE_GET = 5
    CMD_DLOCK_CFG_PASSIVE_GET = 6

    def send_command(self, cmd, arg='', dev='dlck'):
        """Send a command to the Doorlock Command Class."""
        super().send_command(cmd, arg=arg, dev=dev)

    def ret_command(self, cmd, arg='', dev='dlck'):
        """Send a command to the Doorlock Command Class that returns data."""
        r = self.zware.zw_api('zwif_' + dev, 'cmd={}&ifd={}'.format(cmd, self.id) + arg)
        if cmd == self.CMD_DLOCK_OP_ACTIVE_GET or cmd == self.CMD_DLOCK_OP_PASSIVE_GET:
            return r.find('./zwif/' + dev + '_op')
        elif cmd == self.CMD_DLOCK_CFG_ACTIVE_GET or cmd == self.CMD_DLOCK_CFG_PASSIVE_GET:
            return r.find('./zwif/' + dev + '_cfg')
        return r

    def get_status(self, active=False):
        """Get status from the Doorlock Command Class."""
        cmd = self.CMD_DLOCK_OP_ACTIVE_GET if active else self.CMD_DLOCK_OP_PASSIVE_GET
        sts_lock_door = self.ret_command(cmd)
        self.status = (int(sts_lock_door.get('mode')) == self.CMD_CLOSE_DOOR)
        return {'is_locked': self.status}

    def lock(self):
        """Operate the Doorlock Command Class to lock."""
        self.send_command(self.CMD_DLOCK_SETUP)  # Select this Command Class.
        self.send_command(self.CMD_DLOCK_OP_SET, '&mode=' + str(self.CMD_CLOSE_DOOR))

    def unlock(self):
        """Operate the Doorlock Command Class to unlock."""
        self.send_command(self.CMD_DLOCK_SETUP)  # Select this Command Class.
        self.send_command(self.CMD_DLOCK_OP_SET, '&mode=' + str(self.CMD_OPEN_DOOR))


class zwLockLogging(zwInterface):
    """Representation of a Z-Wave Lock Logging Command Class."""
    CMD_DLOCK_LOG_ACTIVE_GET = 2
    CMD_DLOCK_LOG_PASSIVE_GET = 3
    CMD_DLOCK_LOG_SUP_ACTIVE_GET = 2
    CMD_DLOCK_LOG_SUP_PASSIVE_GET = 3

    def send_command(self, cmd, arg='', dev='dlck_log'):
        """Send a command to the Doorlock Command Class."""
        super().send_command(cmd, arg=arg, dev=dev)

    def ret_command(self, cmd, arg='', dev='dlck_log'):
        """Send a command to the Doorlock Command Class that returns data."""
        r = self.zware.zw_api('zwif_' + dev, 'cmd={}&ifd={}'.format(cmd, self.id) + arg)
        if cmd == self.CMD_DLOCK_LOG_SUP_ACTIVE_GET or cmd == self.CMD_DLOCK_LOG_SUP_PASSIVE_GET:
            return r.find('./zwif/' + dev + '_sup')
        return r


class zwScheduleEntry(zwInterface):
    """
    Representation of a Z-Wave Schedule Entry Lock Command Class.
    Not supported by Z-Ware API yet.
    """

    def send_command(self, cmd, arg='', dev=''):
        """Send a command to the Schedule Entry Lock Command Class."""
        raise NotImplementedError

    def ret_command(self, cmd, arg='', dev=''):
        """Send a command to the Schedule Entry Lock Command Class that returns data."""
        raise NotImplementedError