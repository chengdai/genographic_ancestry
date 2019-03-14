for i in {1..22}; \
do echo Running chromosome ${i} && python calculate_tract_length.py \
--viterbi_file ./AMR_AFR_subset/ibd_cluster_classified/rfmix_outputs/NG_AMR_AFR_subset_1000G_108001_chr${i}.rfmix.0.Viterbi.txt.gz \
--sample_file ./AMR_AFR_subset/ibd_cluster_classified/NG_ibd_classified_AMR_AFR.txt \
--map_file ./AMR_AFR_subset/ibd_cluster_classified/rfmix_inputs/NG_AMR_AFR_subset_1000G_108001_chr${i}.map \
--out_path ./AMR_AFR_subset/ibd_cluster_classified/collapse_ancestry/ \
--ancestry_seq EUR,AFR,AMR \
--chromosome ${i}; done
