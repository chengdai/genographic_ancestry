Scripts in this folder were used to infer IBD tracts using IBDseq and build a haplotype networks (by calculating cumulative IBD across chromosomes)

- `get_ibd_lengths.py` converts IBDseq outputs into cM tracts
- `merge_networks_sum.py` combines IBD segments across chromosomes to get cumulative IBD
- `sparse2edgelist.py` converts the scipy sparse of `merge_networks_sum.py` into a edge list
- `reverse_reindex.py` converts the index IDs generated by `merge_networks_sum.py` back to sample IDs based on mapping provided by `merge_networks_sum.py`

