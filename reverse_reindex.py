import pandas
import sys
import gzip

def reverse_index(merged_graph, reindex_map):
    reindexed = {}
    with open(reindex_map, 'r') as map:
	for line in map:
	    reindexed[int(line.split()[0])] = line.split()[1]
    results = gzip.open(merged_graph, 'r')
    reindexed_results = gzip.open(merged_graph.split('.txt')[0]+'_node_id.txt.gz', 'w')
    batch_size = 10000000
    batch = []
    for line in results:
        batch.append('\t'.join([str(reindexed[int(line.split(',')[0])]), str(reindexed[int(line.split(',')[1])]), line.split(',')[2]]))
	if len(batch) == batch_size:
	    reindexed_results.writelines(batch)
	    batch = []
    reindexed_results.writelines(batch)
    batch = []
    results.close()
    reindexed_results.close()
    
def main():
    reindex_map = sys.argv[1]
    merged_graph = sys.argv[2]
    
    reverse_index(merged_graph, reindex_map)

main()

