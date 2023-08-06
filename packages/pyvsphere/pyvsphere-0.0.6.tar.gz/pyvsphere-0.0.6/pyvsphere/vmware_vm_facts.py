try:
    from pyVmomi import vim
except ImportError:
    pass

from ansible.modules.cloud.vmware.vmware_vm_info import VmwareVmInfo
from .mymodule import AnsibleModule
from .vcenter import VcenterConfig


def vmware_vm_facts(VcenterConfig: VcenterConfig,*args, **kwargs):
    '''
    return list
    [
        {
            'attributes': {},
            'cluster': None,
            'esxi_hostname': '',
            'guest_fullname': '',
            'guest_name': '',
            'ip_address': '',
            'mac_address': [''],
            'power_state': str.,
            'uuid': str,
            'vm_network': dict,
    ]

    '''

    argument_spec = {
        'vm_type': 'all',
        'show_attribute': False
    }

    argument_spec.update(**VcenterConfig.as_dict())

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    vmware_vm_facts = VmwareVmInfo(module)
    _virtual_machines = vmware_vm_facts.get_all_virtual_machines()
    # print(_virtual_machines)

    # module.exit_json(changed=False, msg=_virtual_machines)

    return _virtual_machines


