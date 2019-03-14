import sys
import numpy
import gzip

def filter_network(network_file, out_file = None, min_weight = -numpy.inf, max_weight = numpy.inf):
	network = gzip.open(network_file,'r')
	if out_file == None:
		out = gzip.open(network_file.split('.')[0] + '_filtered.txt.gz', 'w')
	else:
		out = gzip.open(out_file,'w')

	batch_size = 20000000
	batch = []
	for line in network:
		weight = float(line.strip().split(',')[2])
		if (weight > min_weight) and (weight < max_weight):
			batch.append(line.replace(',','\t'))
			if len(batch) == batch_size:
				out.writelines(batch)
				batch = []
	out.writelines(batch)
	batch = []
	network.close()
	out.close()

def main():
	if len(sys.argv) == 5:
		[network_file, min_weight, max_weight, out] = sys.argv[1:]
		print 'filtering {0} with min edge weight of {1} and max weight of {2}. output is: {3}'.format(network_file, min_weight, max_weight, out)
		filter_network(network_file, out_file = out, min_weight = float(min_weight), max_weight = float(max_weight))
	elif len(sys.argv) == 4:
                [network_file, min_weight, max_weight] = sys.argv[1:]
		print 'filtering {0} with min edge weight of {1} and max weight of {2}.'.format(network_file, min_weight, max_weight)
                filter_network(network_file, min_weight = float(min_weight), max_weight = float(max_weight))
	elif len(sys.argv) == 3:
                [network_file, min_weight] = sys.argv[1:]
		print 'filtering {0} with min edge weight of {1}.'.format(network_file, min_weight)
                filter_network(network_file, min_weight = float(min_weight))
	else:
		'{} is not informative. Please include a minimum edge weight.'.format(sys.argv)
main()
