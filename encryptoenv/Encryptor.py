from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5


class Encryptor():

    def __init__(self, key):
        self.key = key

    def encrypt_data(self, data):
        cipher = Cipher_PKCS1_v1_5.new(self.key)
        return cipher.encrypt(data.encode())


    def decrypt_data(self, data):
        decipher = Cipher_PKCS1_v1_5.new(self.key)
        return decipher.decrypt(data, None).decode()