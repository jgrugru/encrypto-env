from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5


class Encryptor():

    def __init__(self, pem_key):
        self.pem_key = pem_key

    def encrypt_data(self, data):
        cipher = Cipher_PKCS1_v1_5.new(self.pem_key)
        if cipher.can_encrypt():
            return cipher.encrypt(data.encode())
        else:
            print("ERROR: cannot encrypt with pem.")

    def decrypt_data(self, data):
        decipher = Cipher_PKCS1_v1_5.new(self.pem_key)
        return decipher.decrypt(data, None).decode()
