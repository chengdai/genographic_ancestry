for level in adjusted_clusters2; do cat cluster_pairs_${level}.txt | while read var1 var2; do 
    awk -v clus1=${var1} '{print $1, $1, clus1}' ../${level}/NG_cluster${var1}.txt > pairs/${level}/NG_cluster${var1}_${var2}.inds &&\
    awk -v clus2=${var2} '{print $1, $1, clus2}' ../${level}/NG_cluster${var2}.txt >> pairs/${level}/NG_cluster${var1}_${var2}.inds &&\
    plink -bfile ~/chengdai/backup/chengdai/NG/genomes/NG_108003_final/unphased/bed_files/NG_32589_108003_phased_all_reordered --within pairs/${level}/NG_cluster${var1}_${var2}.inds --fst --out calculated/${level}/NG_cluster${var1}_${var2}
done; done
