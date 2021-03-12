from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from pem import parse_file
from os import path


class PemFileManager():

    def __init__(self, env_path, filename="my_key.pem"):
        self.filename = filename
        self.env_path = env_path
        self.filepath = path.join(self.env_path.get_env_path(), self.filename)

    def gen_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend()
        )
        return private_key

    def gen_pem_file(self):
        pk = self.gen_key()
        pem = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
        with open(self.filepath, 'wb') as pem_out:
            pem_out.write(pem)

    def read_key(self):
        return parse_file(self.filepath)

    def pem_file_exists(self):
        if path.exists(self.filepath):
            return True
        else:
            return False

    def __str__(self):
        return self.filepath
