import sys
import os.path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),
                                             os.path.pardir)))

from encryptoenv.CLI import parse_args

def test_parser():
    print(__name__)
    parser = parse_args(["my_key.pem"])
    print(parser)
    assert(True)