library('igraph')

args = commandArgs(trailingOnly=TRUE)

if (length(args)==0) {
  stop("first arguement is network, second is out file", call.=FALSE)
} else { max_ibd = 3592.8932316357723 #max_ibd was determined by looking at IBD sharing of 0 degree relatedness
}

network_file = args[1] #'NG_unrelated_all_us_cumulative_ibd_min12_max72.txt'
el=read.table(network_file, header = FALSE, sep = '\t')

el[,1]=as.character(el[,1]) #Because the vertex IDs in this dataset are numbers, we make sure igraph knows these should be treated as characters. Otherwise, it'll create problems (see page on data import)
el[,2]=as.character(el[,2])
el=as.matrix(el)
g=graph.edgelist(el[,1:2], directed = FALSE) #We first greate a network from the first two columns, which has the list of vertices
E(g)$weight=as.numeric(el[,3]) / max_ibd #We then add the edge weights to this network by assigning an edge attribute called 'weight'.
clusters = cluster_louvain(g, weights = E(g)$weight)

write.table(c(membership(clusters)), args[2], sep = '\t', col.names = FALSE)
