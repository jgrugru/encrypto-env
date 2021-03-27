# encrypto-env [![Build Status](https://travis-ci.com/jgrugru/encrypto-env.svg?branch=main)](https://travis-ci.com/jgrugru/encrypto-env)
With one command, you can setup and protect your environment variables. Encrypto-env encrypts the *.env* file with an RSA key stored in a pem file. 

# Install
```python
pip3 install encryptoenv
```

# Examples
```python
$ encryptoenv -a "USERNAME=JGRUGRU" "PASSWORD=MYPASS!2314" -E
```
This command:
1. creates an /env/.env file in the current directory.
2. creates "my_key.pem" in /env/my_key.pem
3. adds variables in the *.env* file with the *-a* option
4. the *-E* option encrypts the *.env* file with the specified key, in this case, the default "my_key.pem"


```python
$ python encryptoenv/main.py -h
usage: encrypto-env [options] path

Encrypt the contents of your .env file with an RSA key.

optional arguments:
  -h, --help            show this help message and exit
  -p pem_path, --pem-file pem_path
                        The pem filepath relative to the environment path folder
  --environment-path env_path
                        Default is 'env' dir. This is where the program looks for the pem
  -b, --blank           Create blank .env file
  -a var [var ...], --add-variable var [var ...]
                        Add variables to the .env file
  --clear               Clear the contents of the .env file
  --dot-env-file dot_env_file
                        Specify the name of the .env file
  -l, --list-variables  List the variable names stored in the .env file
  --no-key              Disables creation of my_key.pem file
  -v, --verbose         Verbose ouptut
  --version             show program's version number and exit
  -E, --Encrypt         Encrypt .env file
  -D, --Decrypt         Decrypt .env file