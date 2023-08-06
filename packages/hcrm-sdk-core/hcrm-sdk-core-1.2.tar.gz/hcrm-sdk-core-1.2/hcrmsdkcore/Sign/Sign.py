__author__ = 'feeir'

import binascii
import hashlib
import hmac

class Sign(object):
    def __init__(self, accesskey, secretykey):
        self.accesskey = accesskey
        self.secretykey = bytes(secretykey, 'utf-8')

    def make(self, request_path, params, method='GET'):
        srcStr = method.upper() + request_path + '?' + "&".join(
            k.replace("_", ".") + "=" + str(params[k]) for k in sorted(params.keys()))
        print(srcStr)
        srcStr = bytes(srcStr, 'utf-8')
        hashed = hmac.new(self.secretykey, srcStr, hashlib.sha1)
        return str(binascii.b2a_base64(hashed.digest())[:-1], encoding='utf-8')