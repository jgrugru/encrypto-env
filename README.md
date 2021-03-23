# encrypto-env
Easily setup your Python .env file with encryption.

With one command, you can setup your environment variables inside your Python project. Encrypto-env encrypts the *.env* file with a key (a pem file). 


```python
$ python encryptoenv/main.py -h
usage: encrypto-env [options] path

Encrypt the contents of your .env file with an RSA key.

positional arguments:
  pem_filename          The pem filepath relative to the environment path folder

optional arguments:
  -h, --help            show this help message and exit
  -e env_path, --environment-path env_path
                        Default is 'env' dir. This is where the program looks for the pem.
  -b, --blank           Create blank .env file.
  -a var [var ...], --add-variable var [var ...]
                        Add variables to the .env file.
  --clear               Clear the contents of the .env file
  --envfile name        Specify the name of the '.env' file.
  -v, --verbose         Verbose ouptut
  --version             show program's version number and exit
  -E, --Encrypt         Encrypt .env file.
  -D, --Decrypt         Decrypt .env file.
  ```