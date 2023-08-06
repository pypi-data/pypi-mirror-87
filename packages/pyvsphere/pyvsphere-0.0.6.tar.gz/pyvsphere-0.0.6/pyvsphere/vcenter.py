


class VcenterConfig:

    def __init__(self,hostname,username,password,validate_certs=False,port=443):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.validate_certs = validate_certs
        self.port = port

    def as_dict(self):
        return self.__dict__



if __name__ == '__main__':

    v = VcenterConfig(hostname='',username='',password='',validate_certs='',port='')
    print(v.__dict__)
    print(v.as_dict())