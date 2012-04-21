#! /usr/bin/env python

from jpegglitcher import JpegGlitcher

def main():
    parser = JpegGlitcher("landscape.jpeg")
    parser.parse_file()
    parser.find_parts()
    parser.huffman_glitch()
    parser.output_file("test.jpg")

if __name__ == "__main__":
    main()
