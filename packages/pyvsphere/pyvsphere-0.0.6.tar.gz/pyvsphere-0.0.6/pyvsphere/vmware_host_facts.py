
from ansible.modules.cloud.vmware.vmware_host_facts import VMwareHostFactManager
from .mymodule import AnsibleModule
from .vcenter import VcenterConfig

try:
    from pyVmomi import vim
except ImportError:
    pass



class MyVMwareHostFactManager(VMwareHostFactManager):

    def all_facts(self):
        ansible_facts = {}
        ansible_facts.update(self.get_cpu_facts())
        ansible_facts.update(self.get_memory_facts())
        ansible_facts.update(self.get_datastore_facts())
        ansible_facts.update(self.get_network_facts())
        ansible_facts.update(self.get_system_facts())
        ansible_facts.update(self.get_vsan_facts())
        ansible_facts.update(self.get_cluster_facts())
        return ansible_facts




def vmware_host_facts(VcenterConfig: VcenterConfig,esxi_hostname=None):
    """

    :param VcenterConfig:
    :param esxi_hostname:
    :return: {'ansible_all_ipv4_addresses': ['192.168.10.100'],
     'ansible_bios_date': datetime.datetime(2019, 8, 15, 0, 0, tzinfo=<pyVmomi.Iso8601.TZInfo object at 0x110b36278>),
     'ansible_bios_version': '2.3.10',
     'ansible_datastore': [{'free': '2.63 TB',
                            'name': 'RAID5-SSD',
                            'total': '3.49 TB'},
                           {'free': '2.21 TB',
                            'name': 'office_nas',
                            'total': '8.73 TB'}],
     'ansible_distribution': 'VMware ESXi',
     'ansible_distribution_build': '13981272',
     'ansible_distribution_version': '6.7.0',
     'ansible_hostname': '192.168.10.100',
     'ansible_in_maintenance_mode': False,
     'ansible_interfaces': ['vmk0'],
     'ansible_memfree_mb': 115968,
     'ansible_memtotal_mb': 261588,
     'ansible_os_type': 'vmnix-x86',
     'ansible_processor': 'Intel(R) Xeon(R) Silver 4208 CPU @ 2.10GHz',
     'ansible_processor_cores': 16,
     'ansible_processor_count': 2,
     'ansible_processor_vcpus': 32,
     'ansible_product_name': 'PowerEdge R640',
     'ansible_product_serial': 'xxxxxxx',
     'ansible_system_vendor': 'Dell Inc.',
     'ansible_uptime': 12276850,
     'ansible_vmk0': {'device': 'vmk0',
                      'ipv4': {'address': '192.168.10.50',
                               'netmask': '255.255.255.0'},
                      'macaddress': 'xx:xx:xx:xx:xx:xx',
                      'mtu': 1500},
     'cluster': None,
     'vsan_cluster_uuid': None,
     'vsan_health': 'unknown',
     'vsan_node_uuid': None}
    """
    argument_spec = {}
    argument_spec['esxi_hostname'] = esxi_hostname

    argument_spec.update(**VcenterConfig.as_dict())

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    vm_host_manager = MyVMwareHostFactManager(module)

    return vm_host_manager.all_facts()

