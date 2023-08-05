import pprint


class AnsibleModule:

    def __init__(self, argument_spec, supports_check_mode, *args, **kwargs):
        self.params = argument_spec
        self.supports_check_mode = supports_check_mode

    def exit_json(self, *args, **kwargs):
        # pprint.pprint(kwargs)

        return kwargs

    def fail_json(self, msg=None, *args, **kwargs):
        pprint.pprint(msg)

        raise Exception(msg)

    def get_info(self, data):

        if isinstance(data, list):
            l = data[1]
        elif isinstance(data, dict):
            l = data
        else:
            raise ImportError('類型錯誤 %s' % data)

        pprint.pprint({k: v for k, v in l.items()})