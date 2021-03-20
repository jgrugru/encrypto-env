from Crypto.PublicKey import RSA
from pem import parse_file
from os import path

from .FileObject import FileObject


class PemFile(FileObject):

    def __init__(self, env_path, filename="my_key.pem"):
        self.filename = filename
        self.env_path = env_path
        self.filepath = path.join(env_path, self.filename)

    def gen_key(self):
        return RSA.generate(2048)

    def gen_pem_file(self, verbose_flag):
        key = self.gen_key()

        if(verbose_flag):
            print("Key generated\n", key)

        f = open(self.filepath,'wb')
        f.write(key.export_key('PEM'))
        f.close()

        if(verbose_flag):
            print("The key was saved to " + self.filepath)

    def get_key(self):
        # return parse_file(self.filepath)
        if self.filepath_exists():
            with open(self.filepath,'r') as pem_file:
                key = RSA.import_key(pem_file.read())
        else:
            key = None
            print(self.filepath + " does not exist.")
        
        return key

    def __str__(self):
        return self.filepath
