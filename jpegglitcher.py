
from jpegparser import JpegParser
from random import randint
from struct import pack

class JpegGlitcher(JpegParser):

    def find_parts(self):
        self.huffmans = []
        for p in self.structures:
            if p.tag == '\xC4':
                self.huffmans.append(p)

        self.quantizes = []
        for p in self.structures:
            if p.tag == '\xDB':
                self.quantizes.append(p)

        self.compressed_data = []
        for p in self.structures:
            if p.tag == '\xDA':
                self.compressed_data.append(p)

    def huffman_glitch(self):
        pass

    def quantize_glitch(self):
        pass

    def data_glitch(self):
        for sd in self.compressed_data:
            for i in range(sd.size):
                if randint(1, 10000) < 10:
                    if sd.data[i-1] == '\xFF':
                        sd.data[i-1] = pack('B', randint(1, 254))
                    sd.data[i] = pack('B', randint(1, 254))

