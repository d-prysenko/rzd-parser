from AvitoParser import AvitoParser
# from Product import *

# createTables()

search_str = 'iphone+xs'


def main():
    parser = AvitoParser()
    parser.handleAds(search_str)


if __name__ == "__main__":
    main()
