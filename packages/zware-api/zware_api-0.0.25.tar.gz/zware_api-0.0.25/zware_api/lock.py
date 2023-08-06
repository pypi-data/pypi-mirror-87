from .objects import zwInterface
import asyncio

EVENTS = {
    "0": {
        "9": {
            "1": "Deadbolt jammed while locking",
            "2": "Deadbolt jammed while unlocking",
        },
        "18": {
            "default": "Keypad Lock with user_id {}",
        },
        "19": {
            "default": "Keypad Unlock with user_id {}",
        },
        "21": {
            "1": "Manual Lock by Key Cylinder or Thumb-Turn",
            "2": "Manual Lock by Touch Function",
            "3": "Manual Lock by Inside Button",
        },
        "22": {
            "1": "Manual Unlock Operation",
        },
        "24": {
            "1": "RF Lock Operation",
        },
        "25": {
            "1": "RF Unlock Operation",
        },
        "27": {
            "1": "Auto re-lock cycle complete",
        },
        "33": {
            "default": "Single user code deleted with user_id {}",
        },
        "38": {
            "default": "Non access code entered with user_id {}",
        },
        "96": {
            "default": "Daily Schedule has been set/erased for user_id {}"
        },
        "97": {
            "default": "Daily Schedule has been enabled/disabled for user_id {}"
        },
        "98": {
            "default": "Yearly Schedule has been set/erased for user_id {}"
        },
        "99": {
            "default": "Yearly Schedule has been enabled/disabled for user_id {}"
        },
        "100": {
            "default": "All Schedules have been set/erased for user_id {}"
        },
        "101": {
            "default": "All Schedules have been enabled/disabled for user_id {}"
        },
        "112": {
            "default": "New user code added with user_id {}",
            "0": "Master Code was changed at keypad",
            "251": "Master Code was changed over RF",
        },
        "113": {
            "0": "Duplicate Master Code error",
            "default": "Duplicate Pin-Code error with user_id {}",
        },
        "130": {
            "0": "Door Lock needs Time Set"
        },
        "131": {
            "default": "Disabled user_id {} code was entered at the keypad"
        },
        "132": {
            "default": "Valid user_id {} code was entered outside of schedule"
        },
        "161": {
            "1": "Keypad attempts exceed limit",
            "2": "Front Escutcheon removed from main",
            "3": "Master Code attempts exceed limit",
        },
        "167": {
            "default": "Low Battery Level {}",
        },
        "168": {
            "default": "Critical Battery Level {}",
        }
    },
    "6": {
        "0": "State idle",
        "1": "Manual Lock Operation",
        "2": "Manual Unlock Operation",
        "3": "RF Lock Operation",
        "4": "RF Unlock Operation",
        "5": "Keypad Lock Operation",
        "6": "Keypad Unlock Operation",
        "7": "Manual Not Fully Locked Operation",
        "8": "RF Not Fully Locked Operation",
        "9": "Auto Lock Locked Operation",
        "10": "Auto Lock Not Fully Operation",
        "11": "Lock Jammed",
        "12": "All user codes deleted",
        "13": "Single user code deleted",
        "14": "New user code added",
        "15": "New user code not added due to duplicate code",
        "16": "Keypad temporary disabled",
        "17": "Keypad busy",
        "18": "New Program code Entered - Unique code for lock configuration",
        "19": "Manually Enter user Access code exceeds code limit",
        "20": "Unlock By RF with invalid user code",
        "21": "Locked by RF with invalid user codes",
        "22": "Window/Door is open",
        "23": "Window/Door is closed",
        "24": "Window/door handle is open",
        "25": "Window/door handle is closed",
        "32": "Messaging User Code entered via keypad",
        "64": "Barrier performing Initialization process",
        "65": "Barrier operation (Open / Close) force has been exceeded.",
        "66": "Barrier motor has exceeded manufacturer’s operational time limit",
        "67": "Barrier operation has exceeded physical mechanical limits.",
        "68": "Barrier unable to perform requested operation due to UL requirements",
        "69": "Barrier Unattended operation has been disabled per UL requirements",
        "70": "Barrier failed to perform Requested operation, device malfunction",
        "71": "Barrier Vacation Mode",
        "72": "Barrier Safety Beam Obstacle",
        "73": "Barrier Sensor Not Detected / Supervisory Error",
        "74": "Barrier Sensor Low Battery Warning",
        "75": "Barrier detected short in Wall Station wires",
        "76": "Barrier associated with non-Z-wave remote control",
        "254": "Unknown Event"
    },
    "8": {
        "1": "Door Lock needs Time Set",
        "10": "Low Battery",
        "11": "Critical Battery Level"
    }
}


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
        super(self, zwLock).send_command(cmd, arg=arg, dev=dev)

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
        self.status = (int(sts_lock_door.get('mode')) == self.CMD_OPEN_DOOR)
        return {'is_open': self.status}

    def lock(self):
        """Operate the Doorlock Command Class to lock."""
        self.send_command(self.CMD_DLOCK_SETUP)  # Select this Command Class.
        self.send_command(self.CMD_DLOCK_OP_SET, '&mode=' + str(self.CMD_CLOSE_DOOR))

    def unlock(self, ifd):
        """Operate the Doorlock Command Class to unlock."""
        self.send_command(self.CMD_DLOCK_SETUP)  # Select this Command Class.
        self.send_command(self.CMD_DLOCK_OP_SET, '&mode=' + str(self.CMD_OPEN_DOOR))


class zwBattery(zwInterface):
    """Representation of a Z-Wave Battery Command Class."""
    CMD_BATTERY_ACTIVE_GET = 2
    CMD_BATTERY_PASSIVE_GET = 3

    def send_command(self, cmd, arg='', dev='battery'):
        """Send a command to the Battery Command Class."""
        super(self, zwBattery).send_command(cmd, arg=arg, dev=dev)

    def ret_command(self, cmd, arg='', dev='battery'):
        """Send a command to the Battery Command Class that returns data."""
        return super(self, zwBattery).ret_command(cmd, arg=arg, dev=dev)

    def get_status(self, active=False):
        """Get the battery level of the lock."""
        cmd = self.CMD_BATTERY_ACTIVE_GET if active else self.CMD_BATTERY_PASSIVE_GET
        status = self.ret_command(cmd)
        self.status = int(status.get('level'))
        return {'battery': self.status}


class zwUserCode(zwInterface):
    """Representation of a Z-Wave User Code Command Class."""
    CMD_USER_CODE_ACTIVE_GET = 1
    CMD_USER_CODE_PASSIVE_GET = 2
    CMD_USER_CODE_SET = 3
    CMD_USER_CODE_USERS_ACTIVE_GET = 4
    CMD_USER_CODE_USERS_PASSIVE_GET = 5
    CMD_USER_CODE_MASTER_ACTIVE_GET = 11
    CMD_USER_CODE_MASTER_PASSIVE_GET = 12
    CMD_USER_CODE_MASTER_SET = 13

    STATUS_UNOCCUPIED = 0
    STATUS_OCCUPIED_ENABLED = 1
    STATUS_OCCUPIED_DISABLED = 3
    STATUS_NON_ACCESS_USER = 4

    def send_command(self, cmd, arg='', dev='usrcod'):
        """Send a command to the User Code Command Class."""
        super(self, zwUserCode).send_command(cmd, arg=arg, dev=dev)

    def ret_command(self, cmd, arg='', dev='usrcod'):
        """Send a command to the User Code Command Class that returns data."""
        r = self.zware.zw_api('zwif_' + dev, 'cmd={}&ifd={}'.format(cmd, self.id) + arg)
        if cmd == self.CMD_USER_CODE_ACTIVE_GET or cmd == self.CMD_USER_CODE_PASSIVE_GET:
            return r.find('./zwif/' + dev)
        elif cmd == self.CMD_USER_CODE_USERS_ACTIVE_GET or cmd == self.CMD_USER_CODE_USERS_PASSIVE_GET:
            return r.find('./zwif/usrcod_sup')
        return r

    def get_master_code(self, active=False):
        """Get the master code. Only if the specific devices' User Code Command Class supports it."""
        cmd = self.CMD_USER_CODE_MASTER_ACTIVE_GET if active else self.CMD_USER_CODE_MASTER_PASSIVE_GET
        status = self.ret_command(cmd)
        return {'master_code': status.get('master_code')}

    async def set_master_code(self, code, verify=True):
        """Set the master code. Only if the specific devices' User Code Command Class supports it."""
        try:
            self.send_command(self.CMD_USER_CODE_MASTER_SET, arg='&master_code={}'.format(code))
        except:
            return False
        if verify:
            timeout = 0
            while self.ret_command(self.CMD_USER_CODE_MASTER_ACTIVE_GET).get('master_code') != str(code):
                if timeout >= 20:
                    return False
                await asyncio.sleep(1)
                timeout += 1
        return True

    async def set_codes(self, user_ids: list, status: list, codes=None, verify=True):
        """Set a list of code slots to the given statuses and codes."""
        user_ids = ",".join(user_ids)
        status = ",".join(status)
        codes = ",".join(codes if codes else [])
        try:
            self.send_command(self.CMD_USER_CODE_SET, '&id={}&status={}&code={}'
                              .format(user_ids, status, codes))
        except:
            return False
        if verify:
            timeout = 0
            first_user = user_ids[0]
            first_status = status[0]
            first_code = codes[0]
            while not self.is_code_set(first_user, first_status, first_code):
                # Assume that if the first code was set correctly, all codes were.
                if timeout >= 20:
                    return False
                await asyncio.sleep(1)
                timeout += 1
        return True

    async def remove_single_code(self, user_id, verify=True):
        """Set a single code to unoccupied status."""
        return await self.set_codes([user_id], [self.STATUS_UNOCCUPIED], verify=verify)

    async def disable_single_code(self, user_id, code, verify=True):
        """Set a single code to occupied/disabled status."""
        return await self.set_codes([user_id], [self.STATUS_UNOCCUPIED], codes=[code], verify=verify)

    async def get_all_users(self, active=False):
        """Get a dictionary of the status of all users in the lock."""
        cmd = self.CMD_USER_CODE_USERS_ACTIVE_GET if active else self.CMD_USER_CODE_USERS_PASSIVE_GET
        max_users = int(self.ret_command(cmd).get('user_cnt'))
        users = {}
        for i in range(1, max_users + 1):
            cmd = self.CMD_USER_CODE_ACTIVE_GET if active else self.CMD_USER_CODE_PASSIVE_GET
            code = self.ret_command(cmd, arg='&id={}'.format(i))
            users[str(i)] = {
                "status": code.get('status'),
                "code": code.get('code'),
                "update": code.get('utime'),
            }
        return users

    def is_code_set(self, user_id, status, code):
        """Check if a code and status are set in a given id."""
        code_obj = self.ret_command(self.CMD_USER_CODE_ACTIVE_GET, '&id={}'.format(user_id))
        if status == self.STATUS_UNOCCUPIED:
            return code_obj.get('status') == status
        return code_obj.get('status') == status and code_obj.get('code') == code


class zwAlarm(zwInterface):
    """Representation of a Z-Wave Alarm Command Class."""
    CMD_ALARM_ACTIVE_GET = 2
    CMD_ALARM_PASSIVE_GET = 3

    def send_command(self, cmd, arg='', dev='alrm'):
        """Send a command to the Alarm Command Class."""
        super(self, zwAlarm).send_command(cmd, arg=arg, dev=dev)

    def ret_command(self, cmd, arg='', dev='alrm'):
        """Send a command to the Alarm Command Class that returns data."""
        return super(self, zwAlarm).ret_command(cmd, arg=arg, dev=dev)

    def get_alarm_status(self, alarm_vtype):
        """Get the last alarm status of an specific alarm type."""
        status = self.ret_command(self.CMD_ALARM_ACTIVE_GET, '&vtype={}'.format(alarm_vtype))
        name = self.get_event_description(status.get('vtype'), status.get('ztype'),
                                          status.get('level'), status.get('event'))
        return {'alarm_vtype': status.get('vtype'), 'event_description': name, 'ocurred_at': status.get('utime')}

    def get_last_alarm(self):
        """Get the last alarm registered on the lock."""
        status = self.ret_command(self.CMD_ALARM_PASSIVE_GET, '&ztype=255')
        name = self.get_event_description(status.get('vtype'), status.get('ztype'),
                                          status.get('level'), status.get('event'))
        return {'alarm_vtype': status.get('vtype'), 'event_description': name, 'ocurred_at': status.get('utime')}

    def get_event_description(self, vtype, level, ztype, event):
        """Get the event description given the types and levels."""
        name = EVENTS.get(ztype, dict()).get(event)
        if name is None:
            name = EVENTS["0"][vtype].get(level)
            if name is None:
                name = EVENTS[ztype][vtype]["default"].format(level)
        return name
