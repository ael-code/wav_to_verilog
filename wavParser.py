import sys
import os
from struct import unpack as u
from struct import pack as p
from pprint import pprint

filename = sys.argv[1]
filePath =  os.path.join(os.getcwd(),filename )

with open(filePath, 'rb') as f:
    meta = dict()
    
    tRiff = f.read(4)
    f.seek(8)
    tWave = f.read(4)
    
    if tRiff != "RIFF" or tWave != "WAVE":
        raise Exception("Input file not in wav format: "+ filePath )
    
    f.seek(16)
    meta['chunkSize'] = u('<I',f.read(4))[0] # <
    f.seek(20)
    meta['compression'] = u('<H',f.read(2))[0] # <
    f.seek(22)
    meta['channels'] = u('<H',f.read(2))[0] # <
    f.seek(24)
    meta['sampleRate'] = u('<I',f.read(4))[0] # <
    f.seek(34)
    meta['bitsPerSample'] = u('<H',f.read(2))[0] # <
    f.seek(40)
    meta['size'] = u('<I',f.read(4))[0] # >
    
    print "\n-----------------------------------"
    pprint(meta)
    print "-----------------------------------\n"

    
    f.seek(44)
    bytePerSample = meta['chunkSize']/8
    maxAddress = 65536
    for i in range(0, meta['size']/bytePerSample):
        if(i > maxAddress-1):
            break
        chunk = u('<H',f.read(bytePerSample))[0]
        print "16'b{:0>16b} = 16'b{:0>16b};".format(i,chunk)
    
# 16'bADDRESS_IN_BINARIO = 16'bCONTENUTO_CELLA_IN_BINARIO
# esempio:
# 16'b1111000011110000 : data = 16'b0000000011001100;


# wav_sample
# http://www.mediacollege.com/audio/tone/download/
#
# seek
# https://docs.python.org/2/library/stdtypes.html?highlight=seek#file.seek
#
# Wav spec
# https://ccrma.stanford.edu/courses/422/projects/WaveFormat/
