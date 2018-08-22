from mrjob.job import MRJob


class MRWordCount(MRJob):

    def mapper(self, _, line):
        for word in line.split():
        	yield word, 1

    def reducer(self, key, values):
        yield key, sum(values)

    combiner = reducer


if __name__ == '__main__':
    MRWordCount.run()
