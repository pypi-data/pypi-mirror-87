try:
    from pyVmomi import vim
except ImportError:
    pass

from .mymodule import AnsibleModule
from .vcenter import VcenterConfig
from ansible.modules.cloud.vmware.vmware_resource_pool_info import ResourcePoolInfoManager


def vmware_resource_pool_facts(VcenterConfig: VcenterConfig):
    '''
    return list
    [
        {
             'cpu_allocation_expandable_reservation': "True -> <class 'bool'>",
             'cpu_allocation_limit': "29442 -> <class 'pyVmomi.VmomiSupport.long'>",
             'cpu_allocation_overhead_limit': "None -> <class 'NoneType'>",
             'cpu_allocation_reservation': "29442 -> <class 'pyVmomi.VmomiSupport.long'>",
             'cpu_allocation_shares': "4000 -> <class 'int'>",
             'cpu_allocation_shares_level': "'normal' -> <class 'pyVmomi.VmomiSupport.vim.SharesInfo.Level'>",
             'mem_allocation_expandable_reservation': "True -> <class 'bool'>",
             'mem_allocation_limit': "122745 -> <class 'pyVmomi.VmomiSupport.long'>",
             'mem_allocation_overhead_limit': "None -> <class 'NoneType'>",
             'mem_allocation_reservation': "122745 -> <class 'pyVmomi.VmomiSupport.long'>",
             'mem_allocation_shares': "163840 -> <class 'int'>",
             'mem_allocation_shares_level': "'normal' -> <class "'pyVmomi.VmomiSupport.vim.SharesInfo.Level'>",
             'name': "'Resources' -> <class 'str'>",
             'overall_status': "'green' -> <class 'pyVmomi.VmomiSupport.vim.ManagedEntity.Status'>",
             'owner': "'172.16.10.16' -> <class 'str'>",
             'runtime_cpu_max_usage': "29442 -> <class 'pyVmomi.VmomiSupport.long'>",
             'runtime_cpu_overall_usage': "16401 -> <class 'pyVmomi.VmomiSupport.long'>",
             'runtime_cpu_reservation_used': "0 -> <class 'pyVmomi.VmomiSupport.long'>",
             'runtime_cpu_reservation_used_vm': "0 -> <class 'pyVmomi.VmomiSupport.long'>",
             'runtime_cpu_unreserved_for_pool': '29442 -> <class 'pyVmomi.VmomiSupport.long'>",
             'runtime_cpu_unreserved_for_vm': '29442 -> <class 'pyVmomi.VmomiSupport.long'>",
             'runtime_memory_max_usage': '128712704000 -> <class 'pyVmomi.VmomiSupport.long'>",
             'runtime_memory_overall_usage': '79622569984 -> <class 'pyVmomi.VmomiSupport.long'>",
             'runtime_memory_reservation_used': '1972371456 -> <class 'pyVmomi.VmomiSupport.long'>",
             'runtime_memory_reservation_used_vm': '1972371456 -> <class 'pyVmomi.VmomiSupport.long'>",
             'runtime_memory_unreserved_for_pool': '126740332544 -> <class 'pyVmomi.VmomiSupport.long'>",
             'runtime_memory_unreserved_for_vm': '126740332544 -> <class 'pyVmomi.VmomiSupport.long'>"
        }
    ]
    '''

    argument_spec = {}
    argument_spec.update(**VcenterConfig.as_dict())

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    vmware_rp_mgr = ResourcePoolInfoManager(module)

    return vmware_rp_mgr.gather_rp_info()



