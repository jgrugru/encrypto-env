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
1. creates an _/env_ dir in the current directory.
2. creates _/env/.env_ file in the current directory.
3. creates */env/my_key.pem* 
4. *-a* option adds variables in the *.env* file
5. *-E* option encrypts the *.env* file with the specified key, in this case, the default "my_key.pem"


```
$ python encryptoenv/main.py -h
usage: encrypto-env [options] path

Encrypt the contents of your .env file with an RSA key.

optional arguments:
  -h, --help            show this help message and exit
  -p pem_filepath, --pem-file pem_filepath
                        The pem filepath relative to the environment path folder
  --environment-path env_path
                        Default is 'env' dir. Default dir for RSA key and .env
  -a var [var ...], --add-variable var [var ...]
                        Add variables to the .env file
  --clear               Clear the contents of the .env file
  --dot-env-file dot_env_file
                        The .env filepath relative to the environment path folder
  -v, --verbose         Verbose ouptut
  --version             show program's version number and exit
  -E, --Encrypt         Encrypt .env file
  -D, --Decrypt         Decrypt .env file
  --no-key              Disables creation of my_key.pem file
  -l, --list-variables  List the variable names stored in the .env file
```

## Default paths

By default the encryptoenv will use these default paths:
 * creates *env* dir in the current working directory 
 * creates *my_key.pem*, the RSA key, in the env directory
 * creates *.env*, the file holding the variables, in the env dir

 * cwd/
   * env/
     * my_key.pem
     * .env

## Using Arguments from a txt file

If your _pem_ and _.env_ file are not in the default locations, you may find yourself typing out the filepaths for each command.
To avoid this, your parameters can be stored in a txt file.

You can create a txt file that looks something like this:
```
--environment-path
/home/jgrugru/Desktop/projects/encrypto-env/my_environment/
-p
RSA_KEY.pem
--dot-env-file
ENV
```

You can add these parameters from the text file by using the @ symbol:
```
$ python encryptoenv/main.py @my_parameters.txt
```

I can also add any additional arguments:
```
$ python encryptoenv/main.py @my_parameters.txt -a "USERNAME=jgrugru" -E
```
