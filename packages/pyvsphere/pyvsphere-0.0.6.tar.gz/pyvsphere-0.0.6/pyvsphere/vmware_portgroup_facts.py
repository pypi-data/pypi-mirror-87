#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright: (c) 2018, Abhijeet Kasurde <akasurde@redhat.com>
# Copyright: (c) 2018, Christian Kotte <christian.kotte@gmx.de>
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
module: vmware_portgroup_facts
short_description: Gathers facts about an ESXi host's Port Group configuration
description:
- This module can be used to gather facts about an ESXi host's Port Group configuration when ESXi hostname or Cluster name is given.
version_added: '2.6'
author:
- Abhijeet Kasurde (@Akasurde)
- Christian Kotte (@ckotte)
notes:
- Tested on vSphere 6.5
- The C(vswitch_name) property is deprecated starting from Ansible v2.12
requirements:
- python >= 2.6
- PyVmomi
options:
  policies:
    description:
    - Gather facts about Security, Traffic Shaping, as well as Teaming and failover.
    - The property C(ts) stands for Traffic Shaping and C(lb) for Load Balancing.
    type: bool
    default: false
    version_added: 2.8
  cluster_name:
    description:
    - Name of the cluster.
    - Facts will be returned for all hostsystem belonging to this cluster name.
    - If C(esxi_hostname) is not given, this parameter is required.
  esxi_hostname:
    description:
    - ESXi hostname to gather facts from.
    - If C(cluster_name) is not given, this parameter is required.
extends_documentation_fragment: vmware.documentation
'''

EXAMPLES = r'''
- name: Gather portgroup facts about all ESXi Host in given Cluster
  vmware_portgroup_facts:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
    cluster_name: '{{ cluster_name }}'
  delegate_to: localhost

- name: Gather portgroup facts about ESXi Host system
  vmware_portgroup_facts:
    hostname: '{{ vcenter_hostname }}'
    username: '{{ vcenter_username }}'
    password: '{{ vcenter_password }}'
    esxi_hostname: '{{ esxi_hostname }}'
  delegate_to: localhost
'''

RETURN = r'''
hosts_portgroup_facts:
    description: metadata about host's portgroup configuration
    returned: on success
    type: dict
    sample: {
        "esx01": [
            {
                "failback": true,
                "failover_active": ["vmnic0", "vmnic1"],
                "failover_standby": [],
                "failure_detection": "link_status_only",
                "lb": "loadbalance_srcid",
                "notify": true,
                "portgroup": "Management Network",
                "security": [false, false, false],
                "ts": "No override",
                "vlan_id": 0,
                "vswitch": "vSwitch0",
                "vswitch_name": "vSwitch0"
            },
            {
                "failback": true,
                "failover_active": ["vmnic2"],
                "failover_standby": ["vmnic3"],
                "failure_detection": "No override",
                "lb": "No override",
                "notify": true,
                "portgroup": "vMotion",
                "security": [false, false, false],
                "ts": "No override",
                "vlan_id": 33,
                "vswitch": "vSwitch1",
                "vswitch_name": "vSwitch1"
            }
        ]
    }
'''

from ansible.modules.cloud.vmware.vmware_portgroup_info import PortgroupInfoManager
from .mymodule import AnsibleModule
from .vcenter import VcenterConfig


def vmware_portgroup_facts(VcenterConfig: VcenterConfig,esxi_hostname):
    """
    retutn dict
    {
        '172.16.10.16': [
            {
                'portgroup': 'VM Network',
                'vlan_id': 0,
                'vswitch': 'vSwitch0',
                'vswitch_name': 'vSwitch0'
            },
        ]
    }

    """
    argument_spec = dict(
        cluster_name=False,
        esxi_hostname=esxi_hostname,
        policies=False
    )
    argument_spec.update(**VcenterConfig.as_dict())

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=[
            ['cluster_name', 'esxi_hostname'],
        ],
        supports_check_mode=True
    )

    host_pg_mgr = PortgroupInfoManager(module)
    module.exit_json(changed=False, hosts_portgroup_facts=host_pg_mgr.gather_host_portgroup_info())


    return host_pg_mgr.gather_host_portgroup_info()

