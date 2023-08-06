try:
    from pyVmomi import vim
except ImportError:
    pass

from .mymodule import AnsibleModule
from .vcenter import VcenterConfig
from ansible.modules.cloud.vmware.vmware_datastore_info import VMwareHostDatastore, PyVmomiHelper


def vmware_datastore_facts(VcenterConfig: VcenterConfig, name):
    """

    :param VcenterConfig:
    :param name:
    :return:
    """
    argument_spec = {
        'name': name,
        'datacenter': "Datacenter",
        'cluster': False,
        'gather_nfs_mount_info': False,
        'gather_vmfs_mount_info': False
    }

    argument_spec.update(**VcenterConfig.as_dict())

    module = AnsibleModule(
        argument_spec=argument_spec,
        required_one_of=[
            ['cluster', 'datacenter'],
        ],
        supports_check_mode=True
    )
    result = dict(changed=False)

    pyv = PyVmomiHelper(module)

    if module.params['cluster']:
        dxs = pyv.lookup_datastore_by_cluster()
    elif module.params['datacenter']:
        dxs = pyv.lookup_datastore(confine_to_datacenter=True)
    else:
        dxs = pyv.lookup_datastore(confine_to_datacenter=False)

    vmware_host_datastore = VMwareHostDatastore(module)
    datastores = vmware_host_datastore.build_datastore_list(dxs)

    result['datastores'] = datastores

    # found a datastore
    if datastores:
        # module.exit_json(**result)
        if len(datastores) == 1:
            return datastores[0]
        else:
            return datastores
    else:
        msg = "Unable to gather datastore facts"
        if module.params['name']:
            msg += " for %(name)s" % module.params
        msg += " in datacenter %(datacenter)s" % module.params
