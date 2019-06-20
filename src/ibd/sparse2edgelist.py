import scipy.sparse as sparse
import sys
import gzip

def main():
	in_file = sys.argv[1]
	out_file = sys.argv[2]
	m = sparse.load_npz(in_file).tocoo()
	with gzip.open(out_file, 'w') as edge_list:
		for i in xrange(len(m.data)):
			edge_list.write(str(m.row[i])+','+str(m.col[i])+','+str(m.data[i])+'\n')

main()
