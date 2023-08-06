__author__ = 'feeir'

import requests
import time
from hcrmsdkcore.exception.exceptions import ServerException, ClientException
from hcrmsdkcore.Sign.Sign import Sign

class HcrmCoreClient(object):

    def __init__(self, accesskey, secretykey):
        self.accesskey = accesskey
        self.secretykey = secretykey
        self.endpoint = 'http://127.0.0.1:8000'
        self.get_timestamp()

    def get_timestamp(self):
        '''
        时间戳 timestamp 有效时效2小时
        :param :
        :return:
        '''
        self.timestamp = int(time.time())

    def do_action(self, request_path, params, method):
        '''
        请求函数
        :param method: 请求方法
        :param request_path: 请求路径
        :param params: 请求参数
        :return:  code: 0为成功 state: Success为请求成功 data: 数据
        '''
        sign_obj = Sign(self.accesskey, self.secretykey)
        sign = sign_obj.make(request_path, params, method)
        params.update({'sign': sign})
        print('params:', params)
        try:
            if method.upper() == 'GET':
                rsp = requests.get('{endpoint}{request_path}'.format(
                    endpoint=self.endpoint, request_path=request_path), params=params)
            else:
                rsp = requests.post('{endpoint}{request_path}'.format(
                    endpoint=self.endpoint, request_path=request_path), data=params)
        except Exception as e:
            raise ClientException('doRequest', e)
        if not rsp.ok:
            raise ServerException(
                rsp.status_code,
                rsp.content
            )
        try:
            request_data = rsp.json()
        except Exception as e:
            raise ClientException('Json decoding', e)
        return request_data
