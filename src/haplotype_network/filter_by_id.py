import sys
import numpy
import gzip

def filter_network(network_file, id_list, out_file = None):
        network = gzip.open(network_file,'r')
        if out_file == None:
                out = gzip.open(network_file.split('.')[0] + '_filtered.txt.gz', 'w')
        else:
                out = gzip.open(out_file,'w')

	valid_ids = {}
	with open(id_list) as ids:
		for line in ids:
			valid_ids[line.strip().split()[0]] = True

        batch_size = 2000000
        batch = []
        for line in network:
                id1, id2, weight = line.strip().split()
		if (id1 in valid_ids) and (id2 in valid_ids):
                        batch.append(line)
                        if len(batch) == batch_size:
                                out.writelines(batch)
                                batch = []

        out.writelines(batch)
        batch = []
        network.close()
        out.close()

def main():
	args = sys.argv[1:]
	if len(args) == 2:
		[network_f, id_filter] = args
		'filtering {0} with ids in {1}'.format(network_f, id_filter)
		filter_network(network_f, id_filter)
	if len(args) == 3:
		[network_f, id_filter, out_f] = args
		'filtering {0} with ids in {1}, saving in {2}'.format(network_f, id_filter, out_f)
		filter_network(network_f, id_filter, out_f)
main()

