import sys, getopt, time
from RzdParser import RzdParser
from RzdApiClient import RzdCity
from Train import createTables


def main(argv):

    opts, args = getopt.getopt(argv,":i")

    if ('-i', '') in opts:
        print('Creating tables..')
        createTables()

    parser = RzdParser()
    # parser.handleOffers("2024-09-01T00:00:00", RzdCity.Voronezh, RzdCity.Moscow)
    # time.sleep(1)
    parser.handleOffers("2024-12-29T00:00:00", RzdCity.Moscow, RzdCity.Voronezh)
    # time.sleep(1)
    # parser.handleOffers("2024-07-09T00:00:00")
    # time.sleep(1)
    # parser.handleOffers("2024-07-10T00:00:00")
    # time.sleep(1)
    # parser.handleOffers("2024-07-11T00:00:00")
    # time.sleep(1)
    # parser.handleOffers("2024-07-12T00:00:00")
    # time.sleep(1)
    # parser.handleOffers("2024-07-13T00:00:00")
    # time.sleep(1)
    # parser.handleOffers("2024-07-14T00:00:00")


if __name__ == "__main__":
    main(sys.argv[1:])
