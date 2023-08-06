__author__ = 'feeir'

import requests
import time
from hcrmsdkcore.Client.Client import HcrmCoreClient

class HcrmGeneralRequest(HcrmCoreClient):

    def __init__(self, accesskey, secretykey):
        super().__init__(accesskey, secretykey)


    def general(self, action, method='GET', request_path='/api/OpenApi/General/'):
        '''
        :param method: 请求方法
        :param request_path: 请求路径
        :return:
        '''
        params = {'accesskey': self.accesskey, 'timestamp': self.timestamp, 'action': action}
        rsp = self.do_action(request_path, params, method)
        print(rsp)
        return rsp

if __name__ == '__main__':
    accesskey = 'hcrm-enCQH6DucEwfcNT8'
    secretykey = 't5geRZ1U7nCfBiqz5cLYCC2NsUWjAiSH'
    hcrm_cls = HcrmGeneralRequest(accesskey, secretykey)
    # 获取公有云服务器资源列表
    #hcrm_cls.general('cloud_server_instance', method='GET')
    # 获取私有云服务器资源列表
    #hcrm_cls.general('private_cloud_server_instance', method='GET')
    # 获取MySql资源列表
    hcrm_cls.general('mysql_instance', method='GET')


