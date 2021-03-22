from Crypto.PublicKey import RSA
from os import path

from .FileObject import FileObject


class PemFile(FileObject):
    """
    An abstraction of the 'my_key.pem" file.
    Inherits all the functions from FileObject. Extends 
    the class with functions:
    -GEN_KEY: generates an RSA key
    -GEN_PEM_FILE: calls the gen_key and stores it
    in the pem file
    -GET_KEY: grabs the key from the file and 
    returns the key in a useable format for Crypto.
    """

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

        f = open(self.filepath, 'wb')
        f.write(key.export_key('PEM'))
        f.close()

        if(verbose_flag):
            print("The key was saved to " + self.filepath)

    def get_key(self):
        key = None
        
        if self.filepath_exists():
            with open(self.filepath, 'r') as pem_file:
                key = RSA.import_key(pem_file.read())
        else:
            print(self.filepath + " does not exist.")

        return key
