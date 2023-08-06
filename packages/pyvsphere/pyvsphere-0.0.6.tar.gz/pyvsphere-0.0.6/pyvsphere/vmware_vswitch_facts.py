#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Abhijeet Kasurde <akasurde@redhat.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''
---
module: vmware_vswitch_facts
short_description: Gathers facts about an ESXi host's vswitch configurations
description:
- This module can be used to gather facts about an ESXi host's vswitch configurations when ESXi hostname or Cluster name is given.
- The vSphere Client shows the value for the number of ports as elastic from vSphere 5.5 and above.
- Other tools like esxcli might show the number of ports as 1536 or 5632.
- See U(https://kb.vmware.com/s/article/2064511) for more details.
version_added: '2.6'
author:
- Abhijeet Kasurde (@Akasurde)
notes:
- Tested on vSphere 6.5
requirements:
- python >= 2.6
- PyVmomi
options:
  cluster_name:
    description:
    - Name of the cluster.
    - Facts about vswitch belonging to every ESXi host systems under this cluster will be returned.
    - If C(esxi_hostname) is not given, this parameter is required.
  esxi_hostname:
    description:
    - ESXi hostname to gather facts from.
    - If C(cluster_name) is not given, this parameter is required.
extends_documentation_fragment: vmware.documentation
'''

EXAMPLES = r'''
- name: Gather vswitch facts about all ESXi Host in given Cluster
  vmware_vswitch_facts:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
    cluster_name: '{{ cluster_name }}'
    delegate_to: localhost
  register: all_hosts_vswitch_facts

- name: Gather firewall facts about ESXi Host
  vmware_vswitch_facts:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
    esxi_hostname: '{{ esxi_hostname }}'
    delegate_to: localhost
  register: all_vswitch_facts
'''

RETURN = r'''
hosts_vswitch_facts:
    description: metadata about host's vswitch configuration
    returned: on success
    type: dict
    sample: {
        "10.76.33.218": {
            "vSwitch0": {
                "mtu": 1500,
                "num_ports": 128,
                "pnics": [
                    "vmnic0"
                ]
            },
            "vSwitch_0011": {
                "mtu": 1500,
                "num_ports": 128,
                "pnics": [
                    "vmnic2",
                    "vmnic1"
                    ]
            },
        },
    }
'''

from .mymodule import AnsibleModule
from .vcenter import VcenterConfig
from ansible.modules.cloud.vmware.vmware_vswitch_info import VswitchInfoManager



def vmware_vswitch_facts(VcenterConfig: VcenterConfig,esxi_hostname):
    """Main"""
    argument_spec = dict(
        cluster_name=False,
        esxi_hostname=esxi_hostname,
    )
    argument_spec.update(**VcenterConfig.as_dict())

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    vmware_vswitch_mgr = VswitchInfoManager(module)
    module.exit_json(changed=False, hosts_vswitch_facts=vmware_vswitch_mgr.gather_vswitch_info())

    module.get_info(vmware_vswitch_mgr.gather_vswitch_info())


