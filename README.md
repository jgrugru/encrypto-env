# encrypto-env
Easily setup your Python .env file with encryption.

With one command, you can setup your environment variables inside your Python project. Encrypto-env encrypts the *.env* file with a key (a pem file). 


```python
$ python encryptoenv/main.py -h
usage: encrypto-env [options] path

Encrypt the contents of your .env file with a key stored in a pem file.

positional arguments:
  pem_filename          The pem filepath relative to the env folder

optional arguments:
  -h, --help            show this help message and exit
  -e env_path, --environment-path env_path
                        Default is 'env' dir. This is where the program looks for the pem.
  -E, --Encrypt         Encrypt .env file that already exists.
  -D, --Decrypt         Decrypt .env file and output variables.
  -b, --blank           Create blank .env file if one does not exist.
  -a var [var ...], --add-variable var [var ...]
                        Add variables that will be encrypted to the .env file.
  --clear               Clear the .env file of all variables.
  -n name, --name name  Specify the name of the '.env' file.
  -v, --verbose         Verbose ouptut
  --version             show program's version number and exit
  ```