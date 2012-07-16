#! /usr/bin/env python

from jpegglitcher import JpegGlitcher
import argparse

def main():

    parser = argparse.ArgumentParser(description='A small glitching script')
    parser.add_argument('-i', '--input', default='landscape.jpeg', type=str,
                        help='The input file')
    parser.add_argument('-o', '--output', default='output.jpeg', type=str,
                        help='The output file')

    args = parser.parse_args()

    fp = open(args.input)
    data = fp.read()
    fp.close()

    parser = JpegGlitcher(data)
    parser.parse_data()
    parser.find_parts()
    parser.quantize_glitch(100)

    output = parser.output_data()

    of = open(args.output, 'w')
    of.write(output)
    of.close()

if __name__ == '__main__':
    main()
