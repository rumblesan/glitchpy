
from struct import *

class JpegParser():

    def __init__(self, filename):
        self.filename = filename
        self.structures = []
        self.parsers    = []
        self.setup_parsers()

    def parse_file(self):
        with open(self.filename, "rb") as fp:
            byte = fp.read(1)
            while byte != b"":
                if byte == '\xFF':
                    byte = fp.read(1)
                    self.check_tag(byte, fp)
                byte = fp.read(1)


    def check_tag(self, tag, fp):
        for p in self.parsers:
            if p.parse(tag):
                newstruct = p.get_new()
                newstruct.about()
                newstruct.read_data(fp)
                return True
        return False


    def setup_parsers(self):
        self.parsers.append(SOI())
        self.parsers.append(SOF0())
        self.parsers.append(SOF2())
        self.parsers.append(DHT())
        self.parsers.append(DQT())
        self.parsers.append(SOS())
        self.parsers.append(APP())
        self.parsers.append(COM())
        self.parsers.append(EOI())


class JpegStructure(object):

    def __init__(self):
        self.info = "Base Structure"
        self.data = b""

    def about(self):
        print(self.info)

    def parse(self, tag):
        if tag == self.tag:
            return True
        else:
            return False

    def get_new(self):
        return self.__class__()

    def read_data(self, fp):
        data = fp.read(2)
        size = unpack('>H', data)[0]
        #size of data includes 2 size bytes
        #already read them so want to decrease
        #amount we'll read correctly
        size -= 2
        self.data = fp.read(size)


class SOI(JpegStructure):
    def __init__(self):
        self.tag  = '\xD8'
        self.info = "Start of File"

    def read_data(self, fp):
        pass

    def write_data(self):
        pass

class SOF0(JpegStructure):
    def __init__(self):
        self.tag  = '\xC0'
        self.info = "Start of Baseline Frame"

class SOF2(JpegStructure):
    def __init__(self):
        self.tag  = '\xC2'
        self.info = "Start of Progressive Frame"

class DHT(JpegStructure):
    def __init__(self):
        self.tag  = '\xC4'
        self.info = "Huffman Table"

class DQT(JpegStructure):
    def __init__(self):
        self.tag  = '\xDB'
        self.info = "Quantization Table"

class SOS(JpegStructure):
    def __init__(self):
        self.tag  = '\xDA'
        self.info = "Start of Scan"
        self.header_data = b""

    def read_data(self, fp):
        super(SOS, self).read_data(fp)
        self.header_data = self.data

        #find the size of the rest of the data
        pos = fp.tell()
        byte = fp.read(1)
        i = 1
        while byte != b"":
            if byte == '\xFF':
                next_byte = fp.read(1)
                if next_byte != '\x00':
                    break
                else:
                    i += 1
            if byte == b"":
                print("Real Error Here")
                break
            byte = fp.read(1)
            i += 1

        fp.seek(pos)
        self.data = fp.read(i)

class APP(JpegStructure):
    def __init__(self):
        self.tag  = [0xE0, 0xEF]
        self.info = "App Specific"

    def parse(self, tag):
        tag = unpack('B', tag)[0]
        if tag >= self.tag[0] and tag <= self.tag[1]:
            return True
        else:
            return False


class COM(JpegStructure):
    def __init__(self):
        self.tag  = '\xFE'
        self.info = "Comment"

class EOI(JpegStructure):
    def __init__(self):
        self.tag  = '\xD9'
        self.info = "End of Image"
