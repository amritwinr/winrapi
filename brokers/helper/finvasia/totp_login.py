import json
import pyotp
import base64
import hashlib
import requests
from Crypto import Random
from Crypto.Cipher import AES


class AliceBlueClient:
    BASE_URL = ""

    def __init__(self, userId, password, two_fa, totp_encrypt_key):
        self.userId = userId
        self.two_fa = two_fa
        self.password = password
        self.totp_encrypt_key = totp_encrypt_key

    class CryptoJsAES:
        @staticmethod
        def __pad(data):
            BLOCK_SIZE = 16
            length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
            return data + (chr(length) * length).encode()

        @staticmethod
        def __unpad(data):
            return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

        @classmethod
        def __bytes_to_key(cls, data, salt, output=48):
            assert len(salt) == 8, len(salt)
            data += salt
            key = hashlib.md5(data).digest()
            final_key = key
            while len(final_key) < output:
                key = hashlib.md5(key + data).digest()
                final_key += key
            return final_key[:output]

        @classmethod
        def encrypt(cls, message, passphrase):
            salt = Random.new().read(8)
            key_iv = cls.__bytes_to_key(passphrase, salt, 32 + 16)
            key = key_iv[:32]
            iv = key_iv[32:]
            aes = AES.new(key, AES.MODE_CBC, iv)
            return base64.b64encode(b"Salted__" + salt + aes.encrypt(cls.__pad(message)))

        @classmethod
        def decrypt(cls, encrypted, passphrase):
            encrypted = base64.b64decode(encrypted)
            assert encrypted[0:8] == b"Salted__"
            salt = encrypted[8:16]
            key_iv = cls.__bytes_to_key(passphrase, salt, 32 + 16)
            key = key_iv[:32]
            iv = key_iv[32:]
            aes = AES.new(key, AES.MODE_CBC, iv)
            return cls.__unpad(aes.decrypt(encrypted[16:]))

    def login(self):
        totp = pyotp.TOTP(self.totp_encrypt_key)
        encKey = self._get_encryption_key()

        checksum = self.CryptoJsAES.encrypt(self.password.encode(), encKey.encode()).decode('UTF-8')

        response_data = self._web_login(checksum)
        two_fa_response = self._2fa_login(response_data)

        if two_fa_response.json()["loPreference"] == "TOTP" and two_fa_response.json()["totpAvailable"]:
            totp_response = self._verify_totp(totp, two_fa_response.json()['us'])
            if totp_response.json()["userSessionID"]:
                return "success"
        else:
            return "failed"

    def _get_encryption_key(self):
        url = self.BASE_URL + "/customer/getEncryptionKey"
        payload = json.dumps({"userId": self.userId})
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload, verify=True)
        return response.json()["encKey"]

    def _web_login(self, checksum):
        url = self.BASE_URL + "/customer/webLogin"
        payload = json.dumps({"userId": self.userId, "userData": checksum})
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload, verify=True)
        return response.json()

    def _2fa_login(self, response_data):
        url = self.BASE_URL + "/sso/2fa"
        payload = json.dumps({
            "answer1": self.two_fa,
            "userId": self.userId,
            "sCount": str(response_data['sCount']),
            "sIndex": response_data['sIndex']
        })
        headers = {'Content-Type': 'application/json'}
        response = requests.request("POST", url, headers=headers, data=payload, verify=True)
        return response

    def _verify_totp(self, totp, us_token):
        url = self.BASE_URL + "/sso/verifyTotp"
        payload = json.dumps({"tOtp": totp.now(), "userId": self.userId})
        headers = {
            'Authorization': 'Bearer ' + self.userId + ' ' + us_token,
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", url, headers=headers, data=payload, verify=True)
        return response