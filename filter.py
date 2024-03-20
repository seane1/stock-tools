import sys
from utils import *

def main(args):
    args.pop(0)
    filter_db(args[0])
    return

if __name__ == "__main__":
    main(sys.argv)
