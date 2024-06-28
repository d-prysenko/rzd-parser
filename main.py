import sys, getopt
from RzdParser import RzdParser


def main():
    parser = RzdParser()
    parser.handleOffers("2024-04-25T00:00:00")
    parser.handleOffers("2024-04-26T00:00:00")


if __name__ == "__main__":
    main()
