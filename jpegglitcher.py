
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
        for ht in self.huffmans:
            for i in range(len(ht.group_data)):
                if randint(1, 100) < 2:
                    newval = randint(1, 254)
                    print("Writing " + str(newval) + " to position " + str(i))
                    ht.group_data[i] = pack('B', newval)

    def quantize_glitch(self, glitchPercent=60):
        glitched = False
        for qt in self.quantizes:
            for i in range(3, qt.size - 2): #skip first 3 bytes of data
                if randint(1, 100) < glitchPercent:
                    glitched = True
                    qt.data[i] = pack('B', randint(1, 254))
        return glitched

    def data_rand_glitch(self, glitchPercent=0.1):
        glitchPercent *= 100 #scale glitch percent up
        for sd in self.compressed_data:
            for i in range(sd.size - 2):
                #randint between 1 and 10,000 to give finer grain control
                if randint(1, 10000) < glitchPercent:
                    #if the previous data byte is OxFF then we need to 
                    #randomise that as well.
                    if sd.data[i-1] == '\xFF':
                        sd.data[i-1] = pack('B', randint(1, 254))
                    sd.data[i] = pack('B', randint(1, 254))

    def data_move_glitch(self):
        for sd in self.compressed_data:
            pos1 = randint(1, sd.size-2)
            pos2 = randint(1, sd.size-2)
            size = randint(1, int(sd.size/20))
            if sd.data[pos1-1] == '\xFF':
                sd.data[pos1-1] = pack('B', randint(1, 254))
            for i in range(size):
                sd.data[pos1+i] = sd.data[pos2+i]
            if sd.data[pos2+size] == '\xFF':
                sd.data[pos2+size] = pack('B', randint(1, 254))

    def data_reverse_glitch(self):
        for sd in self.compressed_data:
            pos  = randint(1, sd.size-2)
            size = randint(1, int(sd.size/20))
            templist = sd.data[pos:pos+size]
            templist.reverse()
            for i in range(size):
                sd.data[pos+i] = templist[i]
            for i in range(sd.size - 2):
                if sd.data[i] == '\xFF':
                    sd.data[i+1] = '\x00'


def example():
    from sys import argv

    inFile  = argv[1]
    outFile = argv[2]

    ifp = open(inFile)
    data = ifp.read()
    ifp.close()

    parser = JpegGlitcher(data)
    parser.parse_data()
    parser.find_parts()
    parser.quantize_glitch()

    output = parser.output_data()

    ofp = open(outFile, 'w')
    ofp.write(output)
    ofp.close()

if __name__ == '__main__':
    example()

