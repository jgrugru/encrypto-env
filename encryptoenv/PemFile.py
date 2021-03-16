from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from pem import parse_file
from os import path

from .FileObject import FileObject


class PemFile(FileObject):

    def __init__(self, env_path, filename="my_key.pem"):
        self.filename = filename
        self.env_path = env_path
        self.filepath = path.join(env_path, self.filename)

    def gen_key(self):
        private_key = rsa.generate_private_key(
            public_exponent=65537, key_size=2048, backend=default_backend())
        return private_key

    def gen_pem_file(self, verbose_flag):
        pk = self.gen_key()
        pem = pk.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption())

        if(verbose_flag):
            print("Key generated\n", pem)

        with open(self.filepath, 'wb') as pem_out:
            pem_out.write(pem)
            if(verbose_flag):
                print("The key was saved to " + self.filepath)

    def read_key(self):
        return parse_file(self.filepath)

    def __str__(self):
        return self.filepath
