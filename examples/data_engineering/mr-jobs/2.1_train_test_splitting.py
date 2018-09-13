from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import decimal
import hashlib

class MRTrainTestSplit(MRJob):
    
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol
    
    SUBSET ='train'
    TEST_SIZE = .3
    
    def mapper(self, _, value):
        key = value.get('jobId', 0)
        flag = MRTrainTestSplit._sample(key=key, fraction=self.TEST_SIZE)
        if self.SUBSET == 'train':
            flag = not flag
        if flag:
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
    MRTrainTestSplit.run()