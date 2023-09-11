import sys, getopt
from AvitoParser import AvitoParser
from Product import *


search_str = 'iphone+xs'


def main(argv):
    opts, args = getopt.getopt(argv,":i")

    if ('-i', '') in opts:
        print('Creating tables..')
        createTables()
    
    parser = AvitoParser()
    parser.handleAds(search_str)


if __name__ == "__main__":
    main(sys.argv[1:])
