from distutils.core import setup
from setuptools import find_packages, setup
from pathlib import Path
from io import open
from os import path

HERE = Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name = 'encryptoenv',         # How you named your package folder (MyLib)
    packages = find_packages(exclude=("tests",)),
    version = '0.0.2',      # Start with a small number and increase it with every change you make
    license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description = 'With one command, you can setup and encrypt your environment variables.',   # Give a short description about your library
    author = 'Jeff Gruenbaum',                   # Type in your name
    author_email = 'jeff.gruenbaum@gmail.com',      # Type in your E-Mail
    long_description=README,
    long_description_content_type="text/markdown",
    url = 'https://github.com/jgrugru/encrypto-env',   # Provide either the link to your github or to your website
    keywords = ["encryption", "environment_variables", "env", "dotenv", "python", "environment"],
    install_requires=[
        "fileflamingo==0.0.6",
    ],
    entry_points='''
            [console_scripts]
            encryptoenv=encryptoenv.__main__:main
        ''',
    include_package_data=True,
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
)

