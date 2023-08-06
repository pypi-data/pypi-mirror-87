import time

from . import zwInterface


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
        super().send_command(cmd, arg=arg, dev=dev)

    def ret_command(self, cmd, arg='', dev='usrcod'):
        """Send a command to the User Code Command Class that returns data."""
        r = self.zware.zw_api('zwif_' + dev, 'cmd={}&ifd={}'.format(cmd, self.id) + arg)
        if cmd == self.CMD_USER_CODE_ACTIVE_GET or cmd == self.CMD_USER_CODE_PASSIVE_GET:
            return r.find('./zwif/usrcod')
        elif cmd == self.CMD_USER_CODE_USERS_ACTIVE_GET or cmd == self.CMD_USER_CODE_USERS_PASSIVE_GET:
            return r.find('./zwif/usrcod_sup')
        return r

    def get_master_code(self, active=False):
        """Get the master code. Only if the specific devices' User Code Command Class supports it."""
        cmd = self.CMD_USER_CODE_MASTER_ACTIVE_GET if active else self.CMD_USER_CODE_MASTER_PASSIVE_GET
        status = self.ret_command(cmd)
        return {'master_code': status.get('master_code')}

    def set_master_code(self, code, verify=True):
        """Set the master code. Only if the specific devices' User Code Command Class supports it."""
        self.send_command(self.CMD_USER_CODE_MASTER_SET, arg='&master_code={}'.format(code))
        if verify:
            timeout = 0
            while self.ret_command(self.CMD_USER_CODE_MASTER_ACTIVE_GET).get('master_code') != str(code):
                if timeout >= 20:
                    return False
                time.sleep(1)
                timeout += 1
        return True

    def set_codes(self, user_ids: list, status: list, codes=None, verify=True):
        """Set a list of code slots to the given statuses and codes."""
        first_user = user_ids[0]
        first_status = status[0]
        first_code = codes[0] if codes else None
        user_ids = ",".join(user_ids)
        status = ",".join(status)
        codes = ",".join(codes if codes else [])
        self.send_command(self.CMD_USER_CODE_SET, '&id={}&status={}&code={}'
                              .format(user_ids, status, codes))
        if verify:
            timeout = 0
            while not self.is_code_set(first_user, first_status, first_code):
                # Assume that if the first code was set correctly, all codes were.
                if timeout >= 20:
                    return False
                time.sleep(1)
                timeout += 1
        return True

    def get_code(self, user_id, active=False):
        """Get the code from a user_id and its status."""
        cmd = self.CMD_USER_CODE_ACTIVE_GET if active else self.CMD_USER_CODE_PASSIVE_GET
        status = self.ret_command(cmd, arg='&id={}'.format(user_id))
        if status is None:
            return {"user_id": user_id, "status": self.STATUS_UNOCCUPIED, "code": None, "error": "Not found"}
        return {"user_id": status.get("id"), "status": status.get("status"), "code": status.get("code")}

    def remove_single_code(self, user_id, verify=True):
        """Set a single code to unoccupied status."""
        return self.set_codes([user_id], [str(self.STATUS_UNOCCUPIED)], verify=verify)

    def disable_single_code(self, user_id, code, verify=True):
        """Set a single code to occupied/disabled status."""
        return self.set_codes([user_id], [str(self.STATUS_UNOCCUPIED)], codes=[code], verify=verify)

    def get_all_users(self, active=False):
        """Get a dictionary of the status of all users in the lock."""
        cmd = self.CMD_USER_CODE_USERS_ACTIVE_GET if active else self.CMD_USER_CODE_USERS_PASSIVE_GET
        max_users = int(self.ret_command(cmd).get('user_cnt'))
        users = {}
        for i in range(1, max_users + 1):
            cmd = self.CMD_USER_CODE_ACTIVE_GET if active else self.CMD_USER_CODE_PASSIVE_GET
            code = self.ret_command(cmd, arg='&id={}'.format(i))
            if code is not None:
                users[str(i)] = {
                    "status": code.get('status'),
                    "code": code.get('code'),
                    "update": code.get('utime'),
                }
        return users

    def is_code_set(self, user_id, status, code):
        """Check if a code and status are set in a given id."""
        code_obj = self.ret_command(self.CMD_USER_CODE_ACTIVE_GET, '&id={}'.format(user_id))
        if code_obj is None:
            return False
        if status == str(self.STATUS_UNOCCUPIED):
            return code_obj.get('status') == status
        return code_obj.get('status') == status and code_obj.get('code') == code
