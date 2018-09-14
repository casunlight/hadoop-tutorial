from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import heapq

class MRTopN(MRJob):
    
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol
        
    def __init__(self, args):
        super().__init__(args)
        self.N = 10
        
    def mapper(self, _, value):
        try:
            max_ = float(value['estimatedSalary']['value']['maxValue'])
            min_ = float(value['estimatedSalary']['value']['minValue'])
        except (KeyError, ValueError):
            pass
        else:
            yield _, (max_, min_)
            
    def reducer(self, _, values):
        top_n = []
        for value in values:
            if len(top_n) < self.N:
                heapq.heappush(top_n, value)
            else:
                heapq.heappushpop(top_n, value)
        else:
            for value in top_n:
                yield _, value


if __name__ == '__main__':
    MRTopN.run()