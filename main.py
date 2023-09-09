from AvitoParser import AvitoParser


search_str = 'iphone xs'


def main():
    parser = AvitoParser()
    parser.getAds(search_str)


if __name__ == "__main__":
    main()
