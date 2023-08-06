# -*- coding: utf-8 -*-

#
# Dell EMC OpenManage Ansible Modules
# Version 2.0
# Copyright (C) 2018-2019 Dell Inc. or its subsidiaries. All Rights Reserved.

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

try:
    from omsdk.sdkinfra import sdkinfra
    from omsdk.sdkcreds import UserCredentials
    from omsdk.sdkfile import FileOnShare, file_share_manager
    from omsdk.sdkprotopref import ProtoPreference, ProtocolEnum
    from omsdk.http.sdkwsmanbase import WsManOptions

    HAS_OMSDK = True
except ImportError:
    HAS_OMSDK = False

from ansible.module_utils.remote_management.dellemc.dellemc_idrac import iDRACConnection


def run_get_system_inventory(idrac):
    msg = {}
    msg['changed'] = False
    msg['failed'] = False
    err = False

    try:
        # idrac.use_redfish = True
        idrac.get_entityjson()
        msg['msg'] = idrac.get_json_device()
    except Exception as e:
        err = True
        msg['msg'] = "Error: %s" % str(e)
        msg['failed'] = True
    return msg, err


def dellemc_get_system_inventory(idrac_ip,idrac_user,idrac_passwd,idrac_port):

    try:
        ANSIBALLZ_PARAMS = {
            "idrac_ip": idrac_ip,
            "idrac_user": idrac_user,
            "idrac_password": idrac_passwd,
            "idrac_port": idrac_port,
        }

        with iDRACConnection(ANSIBALLZ_PARAMS) as idrac:
            data, err = run_get_system_inventory(idrac)

        return data['msg']
    except:
        raise Exception('ERROR')


if __name__ == '__main__':
    dellemc_get_system_inventory(
        idrac_ip='171.16.1.1',
        idrac_port='2222',
        idrac_user='cmdb',
        idrac_passwd='123456'
    )()
