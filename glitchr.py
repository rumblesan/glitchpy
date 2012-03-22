#! /usr/bin/env python

import jpeg

def main():
    parser = jpeg.JpegParser("landscape.jpeg")
    parser.parse_file()

if __name__ == "__main__":
    main()
