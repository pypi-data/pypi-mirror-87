from .mymodule import AnsibleModule
from .vcenter import VcenterConfig
from ansible.modules.cloud.vmware.vmware_guest_disk_info import PyVmomiHelper


def vmware_guest_disk_info(VcenterConfig: VcenterConfig, moid: str):
    """

    :param VcenterConfig:
    :param moid:
    :return:
    """
    argument_spec = {
        # "uuid":"ddddded7-04a1-76fc-xxxxxxx",
        'moid': moid,
        "use_instance_uuid": True,
        'folder': False,
        "datacenter": "Datacenter",
    }

    argument_spec.update(**VcenterConfig.as_dict())

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=[
            ['name', 'uuid', 'moid']
        ],
        supports_check_mode=True,
    )

    if module.params['folder']:
        # FindByInventoryPath() does not require an absolute path
        # so we should leave the input folder path unmodified
        module.params['folder'] = module.params['folder'].rstrip('/')

    pyv = PyVmomiHelper(module)
    # Check if the VM exists before continuing
    vm = pyv.get_vm()

    if vm:
        # VM exists
        try:
            # module.exit_json(guest_disk_info=pyv.gather_disk_info(vm))
            return pyv.gather_disk_info(vm)

        except Exception as exc:
            module.fail_json(msg="Failed to gather information with exception : %s" % exc)
    else:
        # We unable to find the virtual machine user specified
        # Bail out
        vm_id = (module.params.get('uuid') or module.params.get('moid') or module.params.get('name'))
        module.fail_json(msg="Unable to gather disk information for non-existing VM %s" % vm_id)

