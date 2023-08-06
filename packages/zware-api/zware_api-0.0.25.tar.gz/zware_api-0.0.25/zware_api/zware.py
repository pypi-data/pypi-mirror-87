# Copyright 2014-2018 Silicon Laboratories Inc.
# The licensor of this software is Silicon Laboratories Inc.  Your use of this software is governed by the terms of  Silicon Labs Z-Wave Development Kit License Agreement.  A copy of the license is available at www.silabs.com.

import requests
import xml.etree.ElementTree as ET


class ZWareApi:
    """The ZWare web API."""

    zware_session = None
    zware_url = ""

    def zw_api(self, uri, parm=''):
        r = self.zware_session.post(self.zware_url + uri, data=parm, verify=False)
        assert r.status_code == 200, "Unexpected response from Z-Ware API: {}".format(r.status_code)
        try:
            x = ET.fromstring(r.text)
        except:
            return r.text

        e = x.find('./error')
        assert e is None, e.text
        return x

    """Network operations"""

    def zw_net_wait(self):
        while int(self.zw_api('zwnet_get_operation').find('./zwnet/operation').get('op')):
            pass

    def zw_net_comp(self, op):
        while op != int(self.zw_api('zwnet_get_operation').find('./zwnet/operation').get('prev_op')):
            pass

    def zw_net_op_sts(self, op):
        while op != int(self.zw_api('zwnet_get_operation').find('./zwnet/operation').get('op_sts')):
            pass

    def zw_net_get_grant_keys(self):
        grant_key = self.zw_api('zwnet_add_s2_get_req_keys').find('./zwnet/security').get('req_key')
        return grant_key

    def zw_net_add_s2_get_dsk(self):
        dsk = self.zw_api('zwnet_add_s2_get_dsk').find('./zwnet/security').get('dsk')
        return dsk

    def zw_net_set_grant_keys(self, grant_key):
        return self.zw_api('zwnet_add_s2_set_grant_keys', 'granted_keys=' + grant_key)

    def zw_net_provisioning_list_add(self, dsk, boot_mode, grant_keys, interval, device_name,
                                     device_location, application_version, sub_version, vendor,
                                     product_id, product_type, status, generic_class, specific_class,
                                     installer_icon, uuid_format, uuid):
        provisioning_list_string = 'dsk=' + dsk
        if device_name != "":
            provisioning_list_string = provisioning_list_string + '&name=' + device_name
        if device_location != "":
            provisioning_list_string = provisioning_list_string + '&loc=' + device_location
        if generic_class != "":
            provisioning_list_string = provisioning_list_string + '&ptype_generic=' + generic_class
        if specific_class != "":
            provisioning_list_string = provisioning_list_string + '&ptype_specific=' + specific_class
        if installer_icon != "":
            provisioning_list_string = provisioning_list_string + '&ptype_icon=' + installer_icon
        if vendor != "":
            provisioning_list_string = provisioning_list_string + '&pid_manufacturer_id=' + vendor
        if product_type != "":
            provisioning_list_string = provisioning_list_string + '&pid_product_type=' + product_type
        if product_id != "":
            provisioning_list_string = provisioning_list_string + '&pid_product_id=' + product_id
        if application_version != "":
            provisioning_list_string = provisioning_list_string + '&pid_app_version=' + application_version
        if sub_version != "":
            provisioning_list_string = provisioning_list_string + '&pid_app_sub_version=' + sub_version
        if interval != "":
            provisioning_list_string = provisioning_list_string + '&interval=' + interval
        if uuid_format != "":
            provisioning_list_string = provisioning_list_string + '&uuid_format=' + uuid_format
        if uuid != "":
            provisioning_list_string = provisioning_list_string + '&uuid_data=' + uuid
        if status != "":
            provisioning_list_string = provisioning_list_string + '&pl_status=' + status
        if grant_keys != "":
            provisioning_list_string = provisioning_list_string + '&grant_keys=' + grant_keys
        if boot_mode != "":
            provisioning_list_string = provisioning_list_string + '&boot_mode=' + boot_mode
        return self.zw_api('zwnet_provisioning_list_add', provisioning_list_string)

    def zw_net_provisioning_list_list_get(self):
        devices_info = self.zw_api('zwnet_provisioning_list_list_get').findall('./zwnet/pl_list/pl_device_info')
        return devices_info

    def zw_net_provisioning_list_remove(self, dsk):
        result = self.zw_api('zwnet_provisioning_list_remove', 'dsk=' + dsk)
        return result

    def zw_net_provisioning_list_remove_all(self):
        result = self.zw_api('zwnet_provisioning_list_remove_all')
        return result

    def zw_net_set_dsk(self, dsk):
        return self.zw_api('zwnet_add_s2_accept', 'accept=1&value=' + dsk)

    def zw_init(self, url='https://127.0.0.1/', user='test_user', pswd='test_password', get_version=True):
        self.zware_session = requests.session()
        self.zware_url = url
        self.zware_session.headers.update({'Content-Type': 'application/x-www-form-urlencoded'})  # apache requires this
        self.zw_api('register/login.php', 'usrname=' + user + '&passwd=' + pswd)
        self.zware_url += 'cgi/zcgi/networks//'
        if get_version:
            return self.zw_api('zw_version')
        else:
            return

    def zw_add_remove(self, cmd):
        return self.zw_api('zwnet_add', 'cmd=' + str(cmd))

    def zw_abort(self):
        return self.zw_api('zwnet_abort', '')

    def zw_nameloc(self, epd, name, location):
        return self.zw_api('zwep_nameloc', 'cmd=1&epd=' + epd + '&name=' + name + '&loc=' + location)

    """ Interfaces """

    def zwif_api(self, dev, ifd, cmd=1, arg=''):
        return self.zw_api('zwif_' + dev, 'cmd=' + str(cmd) + '&ifd=' + str(ifd) + arg)

    def zwif_api_ret(self, dev, ifd, cmd=1, arg=''):
        r = self.zwif_api(dev, ifd, cmd, arg)
        if cmd == 2 or cmd == 3:
            return r.find('./zwif/' + dev)
        return r

    def zwif_basic_api(self, ifd, cmd=1, arg=''):
        return self.zwif_api_ret('basic', ifd, cmd, arg)

    def zwif_switch_api(self, ifd, cmd=1, arg=''):
        return self.zwif_api_ret('switch', ifd, cmd, arg)

    def zwif_level_api(self, ifd, cmd=1, arg=''):
        return self.zwif_api_ret('level', ifd, cmd, arg)

    def zwif_thermo_list_api(self, dev, ifd, cmd=1, arg=''):
        r = self.zwif_api_ret('thrmo_' + dev, ifd, cmd, arg)
        if cmd == 5 or cmd == 6:
            return r.find('./zwif/thrmo_' + dev + '_sup')
        return r

    def zwif_thermo_mode_api(self, ifd, cmd=1, arg=''):
        return self.zwif_thermo_list_api('md', ifd, cmd, arg)

    def zwif_thermo_state_api(self, ifd, cmd=1, arg=''):
        return self.zwif_api_ret('thrmo_op_sta', ifd, cmd, arg)

    def zwif_thermo_setpoint_api(self, ifd, cmd=1, arg=''):
        return self.zwif_thermo_list_api('setp', ifd, cmd, arg)

    def zwif_thermo_fan_mode_api(self, ifd, cmd=1, arg=''):
        return self.zwif_thermo_list_api('fan_md', ifd, cmd, arg)

    def zwif_thermo_fan_state_api(self, ifd, cmd=1, arg=''):
        return self.zwif_api_ret('thrmo_fan_sta', ifd, cmd, arg)

    def zwif_meter_api(self, ifd, cmd=1, arg=''):
        return self.zwif_api_ret('meter', ifd, cmd, arg)

    def zwif_bsensor_api(self, ifd, cmd=1, arg=''):
        return self.zwif_api_ret('bsensor', ifd, cmd, arg)

    def zwif_sensor_api(self, ifd, cmd=1, arg=''):
        return self.zwif_api_ret('sensor', ifd, cmd, arg)

    def zwif_av_api(self, ifd, cmd=1, arg=''):
        r = self.zwif_api('av', ifd, cmd, arg)
        if cmd == 2 or cmd == 3:
            return r.find('./zwif/av_caps')
        return r
