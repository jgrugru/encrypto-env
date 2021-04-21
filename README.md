# encrypto-env [![Build Status](https://travis-ci.com/jgrugru/encrypto-env.svg?branch=main)](https://travis-ci.com/jgrugru/encrypto-env)
With one command, you can setup and encrypt your environment variables. 

# :pill: Install
```python
pip3 install encryptoenv
```

 * [Examples](https://github.com/jgrugru/encrypto-env#hamburger-examples)
 * [Default Paths](https://github.com/jgrugru/encrypto-env#open_file_folder-default-paths)
 * [Using Arguments from a txt File](https://github.com/jgrugru/encrypto-env#open_file_folder-default-paths)

# What is it?
Encrypto-env is a cli tool that makes it easy to setup, encrypt, and access environment variables
for your personal projects. To encrypt the *.env* file, an RSA key is used (stored in a pem file).
The user can then access the environment variables by specifying the location
of the _.env_ file and RSA key in their own program.

By default, when the encrpytoenv command is run, the following files will be created:

 * cwd/
   * env/
     * my_key.pem
     * .env

 1. creates *env* directory in the current working directory 
 2. creates *my_key.pem*, the RSA key, in the _env_ directory
 3. creates *.env*, the file holding the variables, in the _env_ directory

# :hamburger: How to Use the CLI Tool

#### Basic Use Case
```python
$ encryptoenv -a "USERNAME=jgrugru" "PASSWORD=Password1234" -E
```
This command:
1. creates an _./env_ dir in the current directory.
2. creates _./env/.env_ file in the current directory.
3. creates *./env/my_key.pem*
4. *-a* option adds variables in the *.env* file
5. *-E* option encrypts the *.env* file with the specified key, in this case, the default "my_key.pem"

#### Accessing the Variables
Once encrypted, your variables can be accessed within your own program after adding
one line of code. 
```python
from encryptoenv.EnvFile import EnvFile

EnvFile().create_environment_variables()

print(environ["USERNAME"])
```
If all the files are in the default location and the _env/_ file is in your current
working directory, you can add the line of code above without any chances. If your
files are not in the default location, you can specify each path or specify
only the environment path if the filenames are the same.
```python
EnvFile(environment_path='.\ENV\').create_environment_variables()
```
If you need to set the _.env_ filename or _pem_ filename, you can do so through key word arguments:
```python
EnvFile(environment_path='.\ENV\', filename='env.txt', pem_filename='RSA_KEY.pem').create_environment_variables()
```


#### Argument Options
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


## :pushpin: Using Arguments from a txt file

If your _pem_ and _.env_ file are not in the default locations, you may find yourself
typing out the filepaths for each command repeatedly.
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

You can also add additional arguments:
```
$ python encryptoenv/main.py @my_parameters.txt -a "USERNAME=jgrugru" -E
```
