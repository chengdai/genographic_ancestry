import glob
import subprocess
import gzip
import datetime
import sys
from scipy import sparse
import pandas


def download_network(network_file):
	#download network
	command = 'wget {0}'.format(network_file)
	final = subprocess.Popen(command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
	(stdout, stderr) = final.communicate()
	#print stdout
	print stderr
	return None

def write_log(network, log_file):
	with open(log_file, 'a+') as log:
		log.write(network + '\t' + datetime.datetime.now().strftime("%m/%d/%Y-%H:%M:%S") + '\n')
	log.close()
	return None

def remove_network(network):
	rm_command = 'rm {0}'.format(network)
	rm_final = subprocess.Popen(rm_command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=True)
	(rm_stdout, rm_stderr) = rm_final.communicate()
	print rm_stdout
	print rm_stderr


def main():
	#import file containing the absolute path to all of the tissue network files to merge
	#one line for tissue network file's absolute path
	#network_list_file = sys.argv[1]

	#prefix fo the merged network file
	merged_network_prefix = sys.argv[1]

	#import list of all tissues
	networks = glob.glob(merged_network_prefix + '*ibd.length')
	#with open(network_list_file, 'r') as f:
	#	networks.extend(f.read().splitlines())
	#f.close()

	#initalize a 35,000 x 35,000 sparse matrix as graph representation
	graph = sparse.lil_matrix((35000,35000))
	#keep a dictionary mapping each edge to its index in the sparse matrix
	reindex = {}


	#operate on network by network
	for network in networks:
		#giant_url = 'http://giant.princeton.edu/static//networks/'
		#network_file = giant_url+network

		#download network
		#print 'downloading network file: {0} \n'.format(network)
		#download_network(network_file)

		#print 'updating graph file {0} using tissue {1} \n'.format(graph_file, network, reindex_file)
		print 'updating graph using {0}'.format(network)

		with open(network, 'r') as tissue:
			for line in tissue:
				gene_A, gene_B, weight = line.strip().split()[0], line.strip().split()[1], float(line.strip().split()[2])

				reindex[gene_A] = reindex.get(gene_A, len(reindex))
				reindex[gene_B] = reindex.get(gene_B, len(reindex))
				
				if reindex[gene_A] < reindex[gene_B]:
					graph[reindex[gene_A], reindex[gene_B]] = graph[reindex[gene_A], reindex[gene_B]] + weight
				elif reindex[gene_B] < reindex[gene_A]:
					graph[reindex[gene_B], reindex[gene_A]] = graph[reindex[gene_B], reindex[gene_A]] + weight


		#write log file
		print 'writing to log file \n'
		write_log(network, merged_network_prefix + '_network_merging.log')

	sparse.save_npz(merged_network_prefix + '_merged_graph.npz', graph.tocsr())

	reverse_reindex = {v: k for k, v in reindex.iteritems()}
	pandas.DataFrame.from_dict(reverse_reindex, orient = 'index').to_csv(merged_network_prefix +'_merged_node_id_map.txt', header = None, sep = '\t')

main()
