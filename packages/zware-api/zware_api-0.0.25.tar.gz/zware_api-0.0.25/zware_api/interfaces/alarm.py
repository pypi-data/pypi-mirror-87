from . import zwInterface

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


def get_event_description(vtype, level, ztype, event):
    """Get the event description given the types and levels."""
    vtype_ev = EVENTS["0"].get(vtype)
    name = None
    if vtype_ev:
        name = vtype_ev.get(level)
        if name is None:
            name = vtype_ev.get("default", "{}").format(level)
    if name is None or name == str(level):
        name = EVENTS.get(ztype, dict()).get(event)
    return name


class zwAlarm(zwInterface):
    """Representation of a Z-Wave Alarm Command Class."""
    CMD_ALARM_ACTIVE_GET = 2
    CMD_ALARM_PASSIVE_GET = 3

    def send_command(self, cmd, arg='', dev='alrm'):
        """Send a command to the Alarm Command Class."""
        super().send_command(cmd, arg=arg, dev=dev)

    def ret_command(self, cmd, arg='', dev='alrm'):
        """Send a command to the Alarm Command Class that returns data."""
        return super().ret_command(cmd, arg=arg, dev=dev)

    def get_alarm_status(self, alarm_vtype):
        """Get the last alarm status of an specific alarm type."""
        status = self.ret_command(self.CMD_ALARM_ACTIVE_GET, '&vtype={}'.format(alarm_vtype))
        name = get_event_description(status.get('vtype'), status.get('ztype'),
                                     status.get('level'), status.get('event'))
        return {'alarm_vtype': status.get('vtype'), 'event_description': name, 'ocurred_at': status.get('utime')}

    def get_last_alarm(self):
        """Get the last alarm registered on the lock."""
        status = self.ret_command(self.CMD_ALARM_PASSIVE_GET, '&ztype=255')
        if status is None:
            return {'event_description': 'Offline'}
        name = get_event_description(status.get('vtype'), status.get('level'),
                                     status.get('ztype'), status.get('event'))
        return {
            'alarm_vtype': status.get('vtype'),
            'alarm_level': status.get('level'),
            'alarm_ztype': status.get('ztype'),
            'alarm_event': status.get('event'),
            'event_description': name,
            'occurred_at': status.get('utime')
        }
