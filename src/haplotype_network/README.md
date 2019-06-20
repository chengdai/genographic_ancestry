The scripts in this file was used to perform Louvain Community Detection on the haplotype network and subsetting larger networks into smaller networks.

- `filter_by_edge_weight.py` is first used to filter the network to the appropriate range of edge weights (12cM - 72 cM)
- `generate_louvain_modules.R` is then used to perform the Louvain method
- `filter_by_id.py` is then used to split the overall network into smaller networks based on sample IDs
