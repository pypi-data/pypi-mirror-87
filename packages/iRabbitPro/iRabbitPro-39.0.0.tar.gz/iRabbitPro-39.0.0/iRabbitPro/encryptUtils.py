#!/usr/bin/python
# -*- coding: utf-8 -*-
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import base64


class RsaUtil:
    def __init__(self, pub_key=None):
        self.pub_key_obj = None
        self.verifier = None
        self.signer = None
        b64_pub_key = RSA.importKey(base64.b64decode(pub_key))
        self.pub_key_obj = Cipher_pkcs1_v1_5.new(b64_pub_key)
        self.verifier = PKCS1_v1_5.new(pub_key)

    def encrypt(self, data_str):
        encrypted_str = base64.b64encode(self.pub_key_obj.encrypt(data_str.encode('utf-8')))
        print(encrypted_str)
        return encrypted_str


if __name__ == '__main__':
    pub_key = 'MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAL7qpP6mG6ZHdDKEIdTqQDo/WQb6NaWftXwOTHnnbnwUEX2/2jI4qALxRWMliYI80cszh6CySbap0KIljDCNDw0CAwEAAQ=='
    data = "test"
    #
    rsa_util = RsaUtil(pub_key)
    print(f'原文: {data}')
    encrypt = rsa_util.encrypt(data)
    print(f'加密: {encrypt}')
