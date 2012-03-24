#! /usr/bin/env python

import jpeg

def main():
    parser = jpeg.JpegParser("landscape.jpeg")
    parser.parse_file()
    parser.output_file("test.jpg")

if __name__ == "__main__":
    main()
