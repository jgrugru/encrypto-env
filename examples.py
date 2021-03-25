# from dotenv import load_dotenv
# load_dotenv("env/.env")


# import os
# token = os.environ.get("api_token")

# print(token)

# trying to find root directory
# import glob
# import os
# import pathlib import Path

# text = glob.glob(Path(os.getcwd()).parent.parent.parent, recursive=True)
# print(text)

"""
import argparse
import os
import sys

my_parser = argparse.ArgumentParser(
    prog='myls',
    usage='%(prog)s [options] path',
    description="List the contents of a directory.",
    epilog='skirt skirt. Emjoy dis porgam. Email: jeff.gruenbaum@gmail.com',
    fromfile_prefix_chars='@')

my_parser.add_argument(
    "Path",
    metavar='path',
    type=str,
    help='The path to the list')

my_parser.add_argument(
    "-l",
    "--long",
    action='store_true',
    help="Enable the long listing format."
)

my_parser.add_argument(
    '-v',
    "--verbose",
    action='store_true',
    help="verbose output")

args = my_parser.parse_args()

input_path = args.Path

if not os.path.isdir(input_path):
    print("The path does not exist")
    sys.exit()

for line in os.listdir(input_path):
    if args.long:
        size = os.stat(os.path.join(input_path, line)).st_size
        line = '%10d %s' % (size, line)
    print(line)
"""


"""
import argparse

my_parser = argparse.ArgumentParser()
my_parser.version = '1.0'
my_parser.add_argument('-a', action="store")
my_parser.add_argument('-b', action='store_const', const=42)
my_parser.add_argument('-c', action='store_true')
my_parser.add_argument('-d', action='store_false')
my_parser.add_argument('-e', action='append')
my_parser.add_argument('-f', action='append_const', const=42)
my_parser.add_argument('-g', action='count')
my_parser.add_argument('-i', action='help')
my_parser.add_argument('-j', action='version')

args = my_parser.parse_args()

print(vars(args))"""


"""import argparse

class VerboseStore(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError('nargs not allowed')
        super(VerboseStore, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print("Here I am, setting the " \
              'values %r for the %r option...' % (values, option_string))
        setattr(namespace, self.dest, values)

my_parser = argparse.ArgumentParser()
my_parser.add_argument(
    '-i',
    '--input',
    action=VerboseStore,
    type=int)

args = my_parser.parse_args()
print(vars(args))"""

"""
import argparse

my_parser = argparse.ArgumentParser()
my_parser.add_argument(
    '-input',
    action='store',
    type=int,
    nargs='+')

args = my_parser.parse_args()

print(args.input)
"""
# print('\n'.join(os.listdir(input_path)))


# if len(sys.argv) > 2:
#     print("you've specified too many agrs")
#     sys.exit()

# if len(sys.argv) < 2:
#     print("You need to specify the path")
#     sys.exit()


# input_path = sys.argv[1]


######################################
# ---------------Unit Test------------
######################################

# from unittest import TestCase

# class TryTesting(TestCase):
#     def test_always_passes(self):
#         self.assertTrue(True)

#     def test_always_fails(self):
#         self.assertTrue(False)

# def test_uppercase():
#     assert "loud noises".upper() == "LOUD NOISES"

# def test_reversed():
#     assert list(reversed([1,2,3,4])) == [4,3,2,1]

# def test_some_primes():
#     assert 37 in {
#         num
#         for num in range(1,50)
#         if num != 1 and not any([num % div == 0 for div in range(2, num)])
#     }

# import pytest

# @pytest.fixture
# def example_people_data():
#     people = [
#         {
#             "given_name": "Alfonsa",
#             "family_name": "Ruiz",
#             "title": "Senior Software Engineer",
#         },
#         {
#             "given_name": "Sayid",
#             "family_name": "Khan",
#             "title": "Project Manager",
#         },
#     ]

#     return people

# def test_format_data_for_excel(example_people_data):
#     pass

# def test_format_data_for_display(example_people_data):
#     pass

import pytest


def is_palindrome(s):
    return s == s[::-1]


@pytest.mark.parametrize("maybe_palindrome, expected_result", [
    ("", True),
    ("a", True),
    ("bob", True),
    ("neveroddoreven", True),
    ("dogeeseseegod", True),
    ("abc", False),
    ("abab", False),
])
def test_is_palindrome(maybe_palindrome, expected_result):
    assert is_palindrome(maybe_palindrome) == expected_result

# @pytest.mark.parametrize("non_palindrome", [
#     "abc",
#     "abab",
# ])
# def test_is_not_palindrome(non_palindrome):
#     assert not is_palindrome(non_palindrome)


# conftest.py file
# ------------------
# import pytest
# import requests

# @pytest.fixture(autouse=True)
# def disable_network_calls(monkeypatch):
#     def stunted_get():
#         raise RuntimeError("Network access not allowed during testing!")
    # monkeypatch.setattr(requests, "get", lambda * args, **kwargs: stunted_get())

# flake8: noqa