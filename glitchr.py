#! /usr/bin/env python

from jpegparser import JpegParser

def main():
    parser = JpegParser("landscape.jpeg")
    parser.parse_file()
    parser.output_file("test.jpg")

if __name__ == "__main__":
    main()
