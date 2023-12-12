import sys, getopt
from RzdParser import RzdParser


def main():
    parser = RzdParser()
    parser.handleOffers()


if __name__ == "__main__":
    main()
