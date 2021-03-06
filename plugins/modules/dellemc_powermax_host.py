#!/usr/bin/python
# Copyright: (c) 2019, DellEMC

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type
ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'
                    }

DOCUMENTATION = r'''
---
module: dellemc_powermax_host
version_added: '1.0.3'
short_description:  Manage host (initiator group) on PowerMax/VMAX Storage
                    System
description:
- Managing hosts on a PowerMax storage system includes creating host with a
  set of initiators and host flags, adding and removing initiators to or from
  host, modifying host flag values, renaming host, and deleting host.
extends_documentation_fragment:
  - dellemc.powermax.dellemc_powermax.powermax
author:
- Vasudevu Lakhinana (@unknown) <ansible.team@dell.com>
- Manisha Agrawal (@agrawm3) <ansible.team@dell.com>

options:
  host_name:
    description:
    - The name of the host. No Special Character support except for _.
      Case sensitive for REST Calls.
    - Creation of an empty host is allowed
    required: true
    type: str
  initiators:
    description:
    - List of Initiator WWN or IQN to be added to the host or removed from the
      host.
    type: list
    elements: str
  state:
    description:
    - Define whether the host should exist or not.
    - present - indicates that the host should exist in the system
    - absent - indicates that the host should not exist in the system
    required: true
    choices: [absent, present]
    type: str
  initiator_state:
    description:
    - Define whether the initiators should be present or absent in the host.
    - present-in-host - indicates that the initiators should exist on host
    - absent-in-host - indicates that the initiators should not exist on host
    - Required when creating a host with initiators or adding and removing
      initiators to or from an existing host
    choices: [present-in-host, absent-in-host]
    type: str
  host_flags:
    description:
    - Input as a yaml dictionary
    - List of all host_flags-
    - 1. volume_set_addressing
    - 2. disable_q_reset_on_ua
    - 3. environ_set
    - 4. avoid_reset_broadcast
    - 5. openvms
    - 6. scsi_3
    - 7. spc2_protocol_version
    - 8. scsi_support1
    - 9. consistent_lun
    - Possible values are true, false, unset(default state)
    required: false
    type: dict
  new_name:
    description:
    - The new name of the host for the renaming function. No Special Character
      support except for _. Case sensitive for REST Calls
    type: str
  '''

EXAMPLES = r'''
  - name: Create host
    dellemc_powermax_host:
      unispherehost: "{{unispherehost}}"
      universion: "{{universion}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      serial_no: "{{serial_no}}"
      host_name: "{{host_name}}"
      initiators:
      - 10000090fa7b4e85
      host_flags:
          spc2_protocol_version: true
          consistent_lun: true
          volume_set_addressing: 'unset'
          disable_q_reset_on_ua: false
          openvms: 'unset'
      state: 'present'
      initiator_state: 'present-in-host'

  - name: Get host details
    dellemc_powermax_host:
      unispherehost: "{{unispherehost}}"
      universion: "{{universion}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      serial_no: "{{serial_no}}"
      host_name: "{{host_name}}"
      state: 'present'

  - name: Adding initiator to host
    dellemc_powermax_host:
      unispherehost: "{{unispherehost}}"
      universion: "{{universion}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      serial_no: "{{serial_no}}"
      host_name: "{{host_name}}"
      initiators:
      - 10000090fa3d303e
      initiator_state: 'present-in-host'
      state: 'present'

  - name: Removing initiator from host
    dellemc_powermax_host:
      unispherehost: "{{unispherehost}}"
      universion: "{{universion}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      serial_no: "{{serial_no}}"
      host_name: "{{host_name}}"
      initiators:
      - 10000090fa3d303e
      initiator_state: 'absent-in-host'
      state: 'present'

  - name: Modify flags of host
    dellemc_powermax_host:
      unispherehost: "{{unispherehost}}"
      universion: "{{universion}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      serial_no: "{{serial_no}}"
      host_name: "{{host_name}}"
      host_flags:
          spc2_protocol_version: unset
          consistent_lun: unset
          volume_set_addressing: true
          disable_q_reset_on_ua: false
          openvms: false
          avoid_reset_broadcast: true
      state: 'present'

  - name: Rename host
    dellemc_powermax_host:
      unispherehost: "{{unispherehost}}"
      universion: "{{universion}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      serial_no: "{{serial_no}}"
      host_name: "{{host_name}}"
      new_name: "{{new_host_name}}"
      state: 'present'

  - name: Delete host
    dellemc_powermax_host:
      unispherehost: "{{unispherehost}}"
      universion: "{{universion}}"
      verifycert: "{{verifycert}}"
      user: "{{user}}"
      password: "{{password}}"
      serial_no: "{{serial_no}}"
      host_name: "{{new_host_name}}"
      state: 'absent'
'''

RETURN = r'''
changed:
    description: Whether or not the resource has changed.
    returned: always
    type: bool
host_details:
    description: Details of the host.
    returned: When host exist.
    type: complex
    contains:
        consistent_lun:
            description: Flag for consistent LUN in host.
            type: bool
        enabled_flags:
            description: List of any enabled port flags overridden by the
                         initiator.
            type: list
        disabled_flags:
            description: List of any disabled port flags overridden by the
                         initiator.
            type: list
        hostId:
            description: Host ID.
            type: str
        hostgroup:
            description: List of host groups that the host is associated with.
            type: list
        initiator:
            description: List of initiators present in the host.
            type: list
        maskingview:
            description: List of masking view in which the host group is
                         present.
            type: list
        num_of_hostgroups:
            description: Number of host groups associated with the host.
            type: int
        num_of_initiators:
            description: Number of initiators present in the host.
            type: int
        num_of_masking_views:
            description: Number of masking views associated with the host.
            type: int
        num_of_powerpath_hosts:
            description: Number of PowerPath hosts associated with the host.
            type: int
        port_flags_override:
            description: Whether any of the initiator port flags are
                         overridden.
            type: bool
        type:
            description: Type of host.
            type: str
'''

import re
import copy
import logging
from ansible_collections.dellemc.powermax.plugins.module_utils.storage.dell \
    import dellemc_ansible_powermax_utils as utils
from ansible.module_utils.basic import AnsibleModule

LOG = utils.get_logger('dellemc_powermax_host', log_devel=logging.INFO)

HAS_PYU4V = utils.has_pyu4v_sdk()

PYU4V_VERSION_CHECK = utils.pyu4v_version_check()

# Application Type
APPLICATION_TYPE = 'ansible_v1.2'


class PowerMaxHost(object):

    '''Class with host(initiator group) operations'''

    u4v_conn = None

    def __init__(self):
        ''' Define all parameters required by this module'''
        self.module_params = utils.get_powermax_management_host_parameters()
        self.module_params.update(self.get_powermax_host_parameters())
        # initialize the ansible module
        self.module = AnsibleModule(
            argument_spec=self.module_params,
            supports_check_mode=False
        )
        # result is a dictionary that contains changed status and host details
        self.result = {"changed": False, "host_details": {}}
        if HAS_PYU4V is False:
            self.show_error_exit(msg="Ansible modules for PowerMax require "
                                 "the PyU4V python library to be "
                                 "installed. Please install the library "
                                 "before using these modules.")

        if PYU4V_VERSION_CHECK is not None:
            self.show_error_exit(msg=PYU4V_VERSION_CHECK)

        if self.module.params['universion'] is not None:
            universion_details = utils.universion_check(
                self.module.params['universion'])
            LOG.info("universion_details: %s", universion_details)

            if not universion_details['is_valid_universion']:
                self.show_error_exit(msg=universion_details['user_message'])

        try:
            self.u4v_conn = utils.get_U4V_connection(
                self.module.params, application_type=APPLICATION_TYPE)
        except Exception as e:
            self.show_error_exit(msg=str(e))
        self.provisioning = self.u4v_conn.provisioning
        self.host_flags_list = {'volume_set_addressing', 'environ_set',
                                'disable_q_reset_on_ua', 'openvms',
                                'avoid_reset_broadcast', 'scsi_3',
                                'spc2_protocol_version', 'scsi_support1'}
        LOG.info('Got PyU4V instance for provisioning on PowerMax ')

    def get_powermax_host_parameters(self):
        return dict(
            host_name=dict(required=True, type='str'),
            initiators=dict(required=False, type='list', elements='str'),
            state=dict(required=True, type='str', choices=['present',
                                                           'absent']),
            initiator_state=dict(required=False, type='str',
                                 choices=['present-in-host',
                                          'absent-in-host']),
            host_flags=dict(required=False, type='dict'),
            new_name=dict(type='str', required=False)
        )

    def get_host(self, host_name):
        '''
        Get details of a given host
        '''
        try:
            LOG.info('Getting host %s details', host_name)
            hostFromGet = self.provisioning.get_host(host_name)
            if hostFromGet:
                return hostFromGet
        except Exception as e:
            LOG.error('Got error %s while getting details of host %s',
                      str(e), host_name)
            return None

    def _set_to_enable(self, host_flag_name, host_flag_dict):
        host_flag_dict[host_flag_name.lower()] = {
            'enabled': True,
            'override': True
        }

    def _set_to_disable(self, host_flag_name, host_flag_dict):
        host_flag_dict[host_flag_name.lower()] = {
            'enabled': False,
            'override': True
        }

    def _set_to_default(self, host_flag_name, host_flag_dict):
        host_flag_dict[host_flag_name.lower()] = {
            'enabled': False,
            'override': False
        }

    def _disable_consistent_lun(self, host_flag_dict):
        host_flag_dict['consistent_lun'] = False

    def _enable_consistent_lun(self, host_flag_dict):
        host_flag_dict['consistent_lun'] = True

    def _create_host_flags_dict(self, received_host_flags,
                                new_host_flags_dict):
        '''
        Creating the expected payload for host_flags
        '''
        for host_flag_name in self.host_flags_list:
            if (host_flag_name not in received_host_flags or
                    received_host_flags[host_flag_name] in ['unset', 'Unset']):
                self._set_to_default(host_flag_name, new_host_flags_dict)

            elif (received_host_flags[host_flag_name] is False or
                  received_host_flags[host_flag_name] in ['false', 'False']):
                self._set_to_disable(host_flag_name, new_host_flags_dict)

            else:
                self._set_to_enable(host_flag_name, new_host_flags_dict)

        if ('consistent_lun' not in received_host_flags
            or received_host_flags['consistent_lun'] is False
            or received_host_flags['consistent_lun'] in ['unset', 'Unset',
                                                         'false', 'False']):
            self._disable_consistent_lun(new_host_flags_dict)

        else:
            self._enable_consistent_lun(new_host_flags_dict)

    def create_host(self, host_name):
        '''
        Create host with given initiators and host_flags
        '''
        initiator_state = self.module.params['initiator_state']
        initiators = self.module.params['initiators']
        received_host_flags = self.module.params['host_flags']

        if (initiator_state == 'absent-in-host' or initiator_state is None):
            initiators = None

        if received_host_flags:
            new_host_flags_dict = {}
            self._create_host_flags_dict(received_host_flags,
                                         new_host_flags_dict)
        else:
            new_host_flags_dict = None

        try:
            msg = ("Creating host %s with parameters:initiators=%s,"
                   "host_flags=%s", host_name, initiators,
                   new_host_flags_dict)
            LOG.info(msg)
            self.provisioning.create_host(host_name,
                                          initiator_list=initiators,
                                          host_flags=new_host_flags_dict)
            return True

        except Exception as e:
            errorMsg = ('Create host %s failed with error %s'
                        % (host_name, str(e)))
            self.show_error_exit(msg=errorMsg)
        return None

    def _get_add_initiators(self, existing, requested):
        all_inits = existing + requested
        add_inits = list(set(all_inits) - set(existing))
        return add_inits

    def _get_remove_initiators(self, existing, requested):
        rem_inits = list(set(existing).intersection(set(requested)))
        return rem_inits

    def add_host_initiators(self, host_name, initiators):
        host = self.get_host(host_name)
        existing_inits = []
        if host and 'initiator' in host:
            existing_inits = host['initiator']

        if initiators and (set(initiators).issubset(set(existing_inits))):
            LOG.info('Initiators are already present in host %s', host_name)
            return False

        add_list = self._get_add_initiators(existing_inits, initiators)
        if len(add_list) > 0:
            try:
                LOG.info('Adding initiators %s to host %s',
                         add_list, host_name)
                self.provisioning.modify_host(host_name,
                                              add_init_list=add_list)
                return True
            except Exception as e:
                errorMsg = (("Adding initiators %s to host %s failed with"
                             "error %s", add_list, host_name, str(e)))
                self.show_error_exit(msg=errorMsg)
        else:
            LOG.info('No initiators to add to host %s', host_name)
            return False

    def remove_host_initiators(self, host_name, initiators):
        host = self.get_host(host_name)
        existing_inits = []
        if host and 'initiator' in host:
            existing_inits = host['initiator']

        if existing_inits is None or not len(existing_inits):
            LOG.info('No initiators are present in host %s', host_name)
            return False

        remove_list = self._get_remove_initiators(existing_inits, initiators)

        if len(remove_list) > 0:
            try:
                LOG.info('Removing initiators %s from host %s',
                         remove_list, host_name)
                self.provisioning.modify_host(host_name,
                                              remove_init_list=remove_list)
                return True
            except Exception as e:
                errorMsg = ("Removing initiators %s from host %s failed"
                            " with error %s", remove_list, host_name, str(e))
                self.show_error_exit(msg=errorMsg)
        else:
            LOG.info('No initiators to remove from host %s', host_name)
            return False

    def rename_host(self, host_name, new_name):
        try:
            self.provisioning.modify_host(host_name, new_name=new_name)
            return True
        except Exception as e:
            errorMsg = ('Renaming of host %s failed with error %s',
                        host_name, str(e))
            self.show_error_exit(msg=errorMsg)
            return None

    def _create_default_host_flags_dict(self, current_flags):
        for flag in self.host_flags_list:
            self._set_to_default(flag, current_flags)

        self._disable_consistent_lun(current_flags)

    def _recreate_host_flag_dict(self, host, current_flags):
        '''
        Recreate current flags dictionary using output from get_host()
        function
        '''
        self._create_default_host_flags_dict(current_flags)

        for flag in host['enabled_flags'].split(','):
            if len(flag) > 0:
                '''
                Remove any extra text from information received from
                get_host() to match the desired input to VMAX python SDK
                '''
                self._set_to_enable(
                    re.sub(
                        r'\(.*?\)',
                        '',
                        flag),
                    current_flags)

        for flag in host['disabled_flags'].split(','):
            if len(flag) > 0:
                self._set_to_disable(
                    re.sub(
                        r'\(.*?\)',
                        '',
                        flag),
                    current_flags)

        if host['consistent_lun'] is False:
            self._disable_consistent_lun(current_flags)
        else:
            self._enable_consistent_lun(current_flags)

    def modify_host_flags(self, host_name, received_host_flags):
        current_flags = {}
        self._recreate_host_flag_dict(self.get_host(host_name), current_flags)
        new_flags_dict = copy.deepcopy(current_flags)

        for flag in received_host_flags:
            if flag != 'consistent_lun':
                if (received_host_flags[flag] is True or
                        received_host_flags[flag] in ['True', 'true']):
                    self._set_to_enable(flag, new_flags_dict)

                elif (received_host_flags[flag] is False or
                      received_host_flags[flag] in ['false', 'False']):
                    self._set_to_disable(flag, new_flags_dict)

                else:
                    self._set_to_default(flag, new_flags_dict)

            elif (received_host_flags['consistent_lun'] is False or
                  received_host_flags['consistent_lun'] in
                  ['False', 'false', 'unset', 'Unset']):
                self._disable_consistent_lun(new_flags_dict)
            else:
                self._enable_consistent_lun(new_flags_dict)

        if new_flags_dict == current_flags:
            LOG.info('No change detected')
            return False
        else:
            try:
                LOG.info('Modifying host flags for host %s with %s',
                         host_name, new_flags_dict)
                self.provisioning.modify_host(host_name,
                                              host_flag_dict=new_flags_dict)
                return True

            except Exception as e:
                errorMsg = ('Modify host %s failed with error %s',
                            host_name, str(e))
                self.show_error_exit(msg=errorMsg)
            return None

    def delete_host(self, host_name):
        '''
        Delete host from system
        A host cannot be deleted if it is associated with a masking view.
        '''
        try:
            self.provisioning.delete_host(host_name)
            return True
        except Exception as e:
            errorMsg = ('Delete host %s failed with error %s',
                        host_name, str(e))
            self.show_error_exit(msg=errorMsg)

    def _create_result_dict(self, changed):
        self.result['changed'] = changed
        if self.module.params['state'] == 'absent':
            self.result['host_details'] = {}
        else:
            if self.module.params['new_name']:
                self.result['host_details'] = self.get_host(
                    self.module.params['new_name'])
            else:
                self.result['host_details'] = self.get_host(
                    self.module.params['host_name'])

    def show_error_exit(self, msg):
        if self.u4v_conn is not None:
            try:
                LOG.info("Closing unisphere connection %s",
                         self.u4v_conn)
                utils.close_connection(self.u4v_conn)
                LOG.info("Connection closed successfully")
            except Exception as e:
                err_msg = ("Failed to close unisphere connection with error:"
                           " %s", str(e))
                LOG.error(err_msg)
        LOG.error(msg)
        self.module.fail_json(msg=msg)

    def perform_module_operation(self):
        '''
        Perform different actions on host based on user parameter
        chosen in playbook
        '''
        state = self.module.params['state']
        intiator_state = self.module.params['initiator_state']
        host_name = self.module.params['host_name']
        initiators = self.module.params['initiators']
        new_name = self.module.params['new_name']
        host_flags = self.module.params['host_flags']

        host = self.get_host(host_name)
        changed = False

        if state == 'present' and not host and host_name:
            LOG.info('Creating host %s', host_name)
            changed = self.create_host(host_name)

        if (state == 'present' and host and intiator_state ==
                'present-in-host' and initiators and len(initiators) > 0):
            LOG.info('Adding initiators to host %s', host_name)
            changed = (self.add_host_initiators(host_name, initiators) or
                       changed)

        if (state == 'present' and host and intiator_state == 'absent-in-host'
                and initiators and len(initiators) > 0):
            LOG.info('Remove initiators from host %s', host_name)
            changed = (self.remove_host_initiators(host_name, initiators)
                       or changed)

        if state == 'present' and host and host_flags:
            LOG.info('Modifying host flags of host %s to %s',
                     host_name, host_flags)
            changed = self.modify_host_flags(host_name, host_flags) or changed

        if state == 'present' and host and new_name:
            if host['hostId'] != new_name:
                LOG.info('Renaming host %s to %s', host_name, new_name)
                changed = self.rename_host(host_name, new_name)

        if state == 'absent' and host:
            LOG.info('Delete host %s ', host_name)
            changed = self.delete_host(host_name) or changed

        self._create_result_dict(changed)
        # Update the module's final state
        LOG.info('changed %s', changed)
        LOG.info("Closing unisphere connection %s", self.u4v_conn)
        utils.close_connection(self.u4v_conn)
        LOG.info("Connection closed successfully")
        self.module.exit_json(**self.result)


def main():
    ''' Create PowerMax host object and perform action on it
        based on user input from playbook'''
    obj = PowerMaxHost()
    obj.perform_module_operation()


if __name__ == '__main__':
    main()
