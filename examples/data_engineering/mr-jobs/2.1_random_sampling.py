from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import decimal
import hashlib

class MRRandomSampling(MRJob):
    
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol
    
    def mapper(self, _, value):
        key = value.get('jobId', 0)
        if MRRandomSampling._sample(key=key, fraction=.1):
            yield _, value
    
    @staticmethod
    def _sample(key, fraction=1):
        if fraction > 1 or fraction < 0:
            raise ValueError('Invalid fraction value')
        frac = decimal.Decimal(str(fraction)).as_tuple()
        numer = sum([v*10**i for i, v in enumerate(frac.digits[::-1])])
        denom = 10**(-frac.exponent)
        hash_val = hashlib.md5(str(key).encode()).hexdigest()
        return (int(hash_val, 16) % denom) < numer
    
        
if __name__ == '__main__':
    MRRandomSampling.run()