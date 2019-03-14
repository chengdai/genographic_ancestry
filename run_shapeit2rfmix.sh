for i in {1..22}; do python ./ancestry_pipeline/shapeit2rfmix.py \
--shapeit_hap_ref ./ref_pop/1000G_108003_top_EUR_chr${i}.hap.gz,\
./ref_pop/1000G_108003_top_AMR_chr${i}.hap.gz,\
./ref_pop/1000G_108003_top_AFR_chr${i}.hap.gz \
--shapeit_hap_admixed ./AMR_AFR_subset/hap_sample_files/NG_108003_AFR_AMR_chr${i}.hap.gz \
--shapeit_sample_ref ./ref_pop/1000G_108003_top_EUR_chr${i}.sample,\
./ref_pop/1000G_108003_top_AMR_chr${i}.sample,\
./ref_pop/1000G_108003_top_AFR_chr${i}.sample \
--shapeit_sample_admixed ./AMR_AFR_subset/hap_sample_files/NG_108003_AFR_AMR_chr${i}.sample \
--ref_keep ./ref_pop/EUR_AMR_AFR.ref \
--admixed_keep ./AMR_AFR_subset/NG_pca_classified_AMR_AFR.txt \
--chr ${i} \
--genetic_map ./genetic_map/genetic_map_chr${i}_combined_b37.txt \
--out ./AMR_AFR_subset/rfmix_inputs/NG_AMR_AFR_subset_1000G_108003; done



