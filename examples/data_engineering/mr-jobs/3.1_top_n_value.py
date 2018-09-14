from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import heapq

class MRTopNValue(MRJob):
    
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol
        
    def configure_args(self):
        super().configure_args()
        self.add_passthru_arg('-n', '--top_n', type=int)
        
    def mapper(self, _, value):
        try:
            max_ = float(value['estimatedSalary']['value']['maxValue'])
            min_ = float(value['estimatedSalary']['value']['minValue'])
        except (KeyError, ValueError):
            pass
        else:
            yield _, (max_, min_)
    
    def reducer_init(self):
        if self.options.top_n < 1:
            raise ValueError('Invalid top_n value')
        self.top_n = []
        
    def reducer(self, _, values):
        for value in values:
            if len(self.top_n) < self.options.top_n:
                heapq.heappush(self.top_n, value)
            else:
                heapq.heappushpop(self.top_n, value)
                
    def reducer_final(self):
        for value in self.top_n:
            yield None, value


if __name__ == '__main__':
    MRTopNValue.run()