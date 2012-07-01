#! /usr/bin/env python

from jpegglitcher import JpegGlitcher

def main():

    fp = open('landscape.jpeg')
    data = fp.read()
    fp.close()

    parser = JpegGlitcher(data)
    parser.parse_data()
    parser.find_parts()
    parser.data_reverse_glitch()

    output = parser.output_data()

    of = open('output.jpg', 'w')
    of.write(output)
    of.close()

if __name__ == '__main__':
    main()
