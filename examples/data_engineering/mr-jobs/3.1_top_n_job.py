from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol

import os
import json

class MRTopNJob(MRJob):
    
    INPUT_PROTOCOL = JSONValueProtocol
    OUTPUT_PROTOCOL = JSONValueProtocol
        
    def __init__(self, args):
        super().__init__(args)
        self.cache_dir = '/home/hadoop/examples/data_engineering/mr-output/'
        self.cache = []
    
    def mapper_init(self):
        for cache_file in os.listdir(self.cache_dir):
            if cache_file.find('part-') == 0:
                with open(os.path.join(self.cache_dir, cache_file), 'r') as f:
                    for line in f:
                        self.cache.append(tuple(json.loads(line)))
        
    def mapper(self, _, value):
        try:
            max_ = float(value['estimatedSalary']['value']['maxValue'])
            min_ = float(value['estimatedSalary']['value']['minValue'])
        except (KeyError, ValueError):
            pass
        else:
            if (max_, min_) in self.cache:
                yield _, value

if __name__ == '__main__':
    MRTopNJob.run()