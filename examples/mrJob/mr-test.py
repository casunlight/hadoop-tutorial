
import json

from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol, RawValueProtocol

class MRWordFrequencyCount(MRJob):
    
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = RawValueProtocol
    
    def mapper(self, _, value):
        yield _, '|'.join(value)

        
if __name__ == '__main__':
    MRWordFrequencyCount.run()